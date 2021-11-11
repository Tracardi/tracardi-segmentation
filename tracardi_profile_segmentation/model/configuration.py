from pydantic import BaseModel


class Configuration(BaseModel):
    segment: str
    action: str = 'add'
    condition: str

