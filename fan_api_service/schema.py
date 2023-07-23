from pydantic import BaseModel


class Capability(BaseModel):
    id: int
    name: str

class Device(BaseModel):
    id: int
    name: str
    #capabilities: list[Capability] = []

class DeviceCreate(BaseModel):
    name: str