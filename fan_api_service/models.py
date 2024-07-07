from typing import List

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

# Database Models

device_capability_table = Table(
    "device_capability",
    Base.metadata,
    Column("device_id", ForeignKey("devices.id")),
    Column("capability_id", ForeignKey("capabilities.id")),
)


class Device(Base):
    __tablename__ = "devices"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), index=True, unique=True)

    capabilities: Mapped[List["Capability"]] = relationship(
        secondary=device_capability_table
    )
    commands: Mapped[list["Command"]] = relationship(back_populates="device")


class Capability(Base):
    __tablename__ = "capabilities"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    command: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(String(120))


class Command(Base):
    __tablename__ = "commands"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, index=True)
    capability_id: Mapped[int] = mapped_column(ForeignKey(Capability.id))
    capability: Mapped[Capability] = relationship()
    device_id: Mapped[str] = mapped_column(ForeignKey(Device.name))
    device: Mapped[Device] = relationship(back_populates="commands")
