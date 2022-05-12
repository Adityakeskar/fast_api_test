from pydantic import BaseModel
from typing import Optional


class BaseAddress(BaseModel):
    address: str
    note: Optional[str]
    latitude: float
    longitude: float


class Address(BaseAddress):
    id: int

    class Config:
        orm_mode = True


class AddressCreate(BaseAddress):

    class Config:
        orm_mode = True


class AddressUpdate(BaseModel):

    __annotations__ = {k: Optional[v] for k, v in BaseAddress.__annotations__.items()}

    class Config:
        orm_mode = True


class RetrieveAddress(BaseModel):

    distance: int
    latitude: int
    longitude: int

    class Config:
        orm_mode = True
