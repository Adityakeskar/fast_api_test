from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from typing import List

from addresses import models, operations as ops, schemas
from app import database


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.post("/addresses/", response_model=schemas.AddressCreate)
def addresses_add(address: schemas.AddressCreate, db: Session=Depends(get_db)):
    return ops.add_address(db=db, address=address)


@app.get("/addresses/", response_model=List[schemas.Address])
def addresses_list(db: Session=Depends(get_db)):
    return ops.get_address_list(db)


@app.get("/addresses/{addr_id}/", response_model=schemas.Address)
def address_detail(addr_id: int, db: Session=Depends(get_db)):
    return ops.get_address(db=db, addr_id=addr_id)


@app.patch("/addresses/{addr_id}/change/", response_model=schemas.AddressUpdate)
def address_change(addr_id: int, address: schemas.AddressUpdate, 
                   db: Session=Depends(get_db)):
    return ops.update_address(db=db, addr_id=addr_id, address=address)


@app.delete("/addresses/{addr_id}/delete/")
def address_delete(addr_id: int, db: Session=Depends(get_db)):
    return ops.delete_address(db=db, addr_id=addr_id)


@app.post("/addresses/retrieve/")
def addresses_retrieve(address: schemas.RetrieveAddress, db: Session = Depends(get_db)):
    return ops.addresses_retrieve(db=db, address=address)
