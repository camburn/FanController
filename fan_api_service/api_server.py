


# / 
# service index page

# /devices/ 
# list all devices

# /devices/{device_id}
# get a specific device and its capabilities

# /devices/{device_id}/capability/{capability_id}
# Action a capability on a device

# /register/
# register a new device

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schema
from .database import session_local, engine

app = FastAPI()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"name": "API Server index page"}

@app.get("/devices/", response_model=list[schema.Device])
def read_devices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    devices = crud.get_devices(db, skip=skip, limit=limit)
    return devices

@app.get("/devices/{device_id}", response_model=schema.Device)
def read_device(device_id: int, db: Session = Depends(get_db)):
    db_device = crud.get_device(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail=f"Device {device_id} not found")
    return db_device

@app.post("/devices/")
def create_device(device: schema.DeviceCreate, db: Session = Depends(get_db)):
    return crud.create_device(db=db, device=device)
