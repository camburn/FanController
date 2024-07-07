from sqlalchemy.orm import Session

from . import schema
from .models import Capability, Command, Device


def get_device(db: Session, name: str) -> Device | None:
    return db.query(Device).filter(Device.name == name).first()


def get_devices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Device).offset(skip).limit(limit).all()


def get_capabilites(db: Session, name: str) -> list[Capability]:
    device = db.query(Device).where(Device.name == name).first()
    return device.capabilities


def create_device(db: Session, device: schema.DeviceCreate) -> Device:

    if db_item := get_device(db, name=device.name):
        return db_item

    db_item = Device(
        name=device.name,
        capabilities=[
            Capability(command=cap.command, description=cap.description)
            for cap in device.capabilities
        ],
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_command(db: Session, command: schema.Command) -> Command:

    db_item = Command(capability_id=command.capability_id, device_id=command.device_id)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_commands(db: Session, device_id: str) -> Command:
    return db.query(Command).filter(Command.device_id == device_id).first()


def delete_command(db: Session, device_id: str, command_id: int) -> bool:
    rows_deleted = (
        db.query(Command)
        .where(Command.id == command_id)
        .delete(synchronize_session="fetch")
    )
    db.commit()
    if rows_deleted == 1:
        return True
    if rows_deleted > 1:
        raise Exception("Deleted multiple commands, this should not be possible")
    return False
