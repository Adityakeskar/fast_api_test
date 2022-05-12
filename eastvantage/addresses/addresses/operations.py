import math
from sqlalchemy.orm import Session

from addresses import models
from addresses import schemas


def get_address(db: Session, addr_id: int):
    return db.query(models.Address).filter(models.Address.id == addr_id)\
        .first()


def get_address_list(db: Session):
    all_addresses = db.query(models.Address).all()  # all objects from table
    if all_addresses:
        return all_addresses 
    

def add_address(db: Session, address: schemas.AddressCreate):
    addr = models.Address(
        address=address.address, note=address.note, latitude=address.latitude,
        longitude=address.longitude)
    db.add(addr)
    db.commit()  # commit changes so that object will be created in table
    db.refresh(addr)
    return addr


def delete_address(db: Session, addr_id: int):
    addr = db.query(models.Address).filter(models.Address.id == addr_id).first()
    db.delete(addr)  # to remove record from table
    db.commit()

    return {"message": "deleted!"}


def update_address(db: Session, addr_id: int, address: schemas.Address):
    addr = db.query(models.Address).filter(models.Address.id == addr_id).first()
    if addr:
        if address.address:
            addr.address = address.address
        
        if address.note:
            addr.note = address.note
        
        if address.latitude: 
            addr.latitude = address.latitude
        
        if address.longitude:
            addr.longitude = address.longitude

        db.commit()
        db.refresh(addr)

        return addr
    else:
        return {"address": "Not Found"}


def addresses_retrieve(db: Session, address: schemas.RetrieveAddress):
    all_addresses = db.query(models.Address).all()
    if all_addresses:
        radius = 6378.1  # Radius of the Earth
        brng = 1.57  # Bearing is 90 degrees converted to radians.
        distance = address.distance  # Distance in km

        lat1 = math.radians(address.latitude)  # Current lat point converted to radians
        lon1 = math.radians(address.longitude)  # Current long point converted to radians

        lat2 = math.asin(math.sin(lat1) * math.cos(distance / radius) +
                         math.cos(lat1) * math.sin(distance / radius) * math.cos(brng))

        lon2 = lon1 + math.atan2(math.sin(brng) * math.sin(distance / radius) * math.cos(lat1),
                                 math.cos(distance / radius) - math.sin(lat1) * math.sin(lat2))

        lat2 = math.degrees(lat2)  # calculated latitude
        lon2 = math.degrees(lon2)  # calculated longitude

        retrieved_addresses = db.query(models.Address).filter(
            models.Address.latitude <= lat2,
            models.Address.longitude <= lon2).all()  # address retrieval on specific conditions
        return retrieved_addresses
    else:
        return []

