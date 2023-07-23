from sqlalchemy.orm import Session
from . import models, schema

def get_device(db: Session, device_id: int):
    return db.query(models.Device).filter(models.Device.id == device_id).first()

def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Device).offset(skip).limit(limit).all()

def create_device(db: Session, device: schema.DeviceCreate):
    db_item = models.Device(**device.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
