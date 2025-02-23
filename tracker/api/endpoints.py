from typing import Annotated

from fastapi import Request, Query
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError

from tracker.service import tracker
from .app import app
from .models import Batch, StatsParams


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
