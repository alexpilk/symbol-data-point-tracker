from pydantic import BaseModel, conlist, conint, field_validator

from tracker.service import tracker


class Batch(BaseModel):
    symbol: str
    values: conlist(float, max_length=10000)


class StatsParams(BaseModel):
    symbol: str
    k: conint(ge=1, le=8)

    @field_validator('symbol')
    @classmethod
    def ensure_symbol_exists(cls, symbol: str):
        if symbol not in tracker.symbols:
            raise ValueError(f'Symbol "{symbol}" does not exist')
        return symbol
