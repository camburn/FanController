from pydantic import BaseModel


class Capability(BaseModel):
    id: int
    command: str
    description: str


class Command(BaseModel):
    device_id: str
    capability_id: int


class CommandResponse(BaseModel):
    command_id: int | None
    command: str | None


class Device(BaseModel):
    id: int
    name: str
    capabilities: list[Capability] = []


class CapabilityCreate(BaseModel):
    command: str
    description: str


class DeviceCreate(BaseModel):
    name: str
    capabilities: list[CapabilityCreate] = []


class Capabilities(BaseModel):
    capabilities: list[Capability] = []
