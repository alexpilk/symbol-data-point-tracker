from collections import defaultdict
from typing import Annotated

from fastapi import FastAPI, Request, Query
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, conlist, conint


class Tracker:
    def __init__(self):
        self.symbols = defaultdict(list)

    def add(self, symbol, values):
        self.symbols[symbol] += (values)

    def get_stats(self, symbol, k):
        values = self.symbols[symbol][-1 * 10 ** k:]
        avg = sum(values) / len(values)
        variance = sum([(point - avg) ** 2 for point in values]) / len(values)
        return {
            'min': min(values),
            'max': max(values),
            'avg': avg,
            'var': variance,
            'last': values[-1]
        }

    def reset(self):
        self.symbols = defaultdict(list)


tracker = Tracker()


class Batch(BaseModel):
    symbol: str
    values: conlist(float, max_length=10000)


class StatsParams(BaseModel):
    symbol: str
    k: conint(ge=1, le=8)


app = FastAPI()


@app.exception_handler(RequestValidationError)
async def hide_input_value_handler(request: Request, exc: RequestValidationError):
    """
    This handler hides the over-sized input list from the error response to ease the load on the network.
    """
    errors = exc.errors()

    for error in errors:
        if error['type'] == 'too_long' and error['loc'] == ('body', 'values'):
            del error['input']

    return await request_validation_exception_handler(request, exc)


@app.post('/add_batch/', status_code=201)
async def add_batch(batch: Batch):
    tracker.add(batch.symbol, batch.values)
    return {
        'data': {
            'symbol': batch.symbol,
            'points_added': len(batch.values),
        }
    }


@app.get('/stats/')
async def get_stats(stats_request: Annotated[StatsParams, Query()]):
    stats = tracker.get_stats(stats_request.symbol, stats_request.k)
    return {
        'data': stats
    }
