from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, conlist


class Batch(BaseModel):
    symbol: str
    values: conlist(float, max_length=10000)


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
    return {
        'data': {
            'symbol': batch.symbol,
            'points_added': len(batch.values),
        }
    }
