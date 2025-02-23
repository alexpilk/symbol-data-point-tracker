from fastapi import FastAPI

from pydantic import BaseModel


class Batch(BaseModel):
    symbol: str
    values: list[float]


app = FastAPI()


@app.post('/add_batch/', status_code=201)
async def add_batch(batch: Batch):
    return {
        'data': {
            'symbol': batch.symbol,
            'points_added': len(batch.values),
        }
    }
