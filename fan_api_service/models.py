
from typing import List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, Mapped
from .database import Base


# Database Models

device_capability_table = Table(
    "device_capability",
    Base.metadata,
    Column("device_id", ForeignKey("devices.id")),
    Column("capability_id", ForeignKey("capabilities.id"))
)


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    capabilities: Mapped[List["Capability"]] = relationship(secondary=device_capability_table)


class Capability(Base):
    __tablename__ = 'capabilities'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)