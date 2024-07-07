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

import logging

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, schema
from .database import Base, engine, session_local

logger = logging.getLogger(__name__)


def logging_configuration():
    logging.basicConfig(level=logging.INFO)


app = FastAPI()
Base.metadata.create_all(engine)
logging_configuration()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"name": "API Server index page"}


@app.get("/devices")
def read_devices(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[schema.Device]:
    devices = crud.get_devices(db, skip=skip, limit=limit)
    return devices


@app.get("/devices/{device_id}")
def read_device(device_id: str, db: Session = Depends(get_db)) -> schema.Device:
    db_device = crud.get_device(db, name=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail=f"Device {device_id} not found")
    return db_device


@app.get("/devices/{device_id}/capabilities")
def get_capababilties(
    device_id: str, db: Session = Depends(get_db)
) -> list[schema.Capability]:
    db_capabilities = crud.get_capabilites(db, name=device_id)
    if db_capabilities is None:
        raise HTTPException(status_code=404, detail=f"Device {device_id} not found")
    print("In URL", db_capabilities)
    return db_capabilities


@app.post("/devices/{device_id}/commands")
def queue_command(command: schema.Command, db: Session = Depends(get_db)):
    crud.create_command(db, command)


@app.get("/devices/{device_id}/commands")
def get_commands(
    device_id: str, db: Session = Depends(get_db)
) -> schema.CommandResponse:
    logger.info(f"Poll Recieved from {device_id}")
    command = crud.get_commands(db, device_id)
    if command:
        logger.info(f"Sending command: {command.capability.command}")
        return {"command_id": command.id, "command": command.capability.command}
    return {"command_id": None, "command": None}


@app.delete("/devices/{device_id}/commands/{command_id}")
def complete_command(device_id: str, command_id: int, db: Session = Depends(get_db)):
    result = crud.delete_command(db, device_id, command_id)
    if result:
        return {"status": "success"}
    return {"status": "error"}


@app.post("/devices")
def create_device(device: schema.DeviceCreate, db: Session = Depends(get_db)):
    dev = crud.create_device(db=db, device=device)
    logging.info(
        f"Successfully registered device with ID: {dev.name}; {len(dev.capabilities)} capabilities"
    )
    return {"registration": "success"}
