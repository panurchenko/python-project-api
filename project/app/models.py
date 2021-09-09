from sqlmodel import SQLModel, Field
from datetime import datetime


class DateTime(SQLModel):
    year: int = datetime.now().year
    month: int = datetime.now().month
    day: int = datetime.now().day
    hour: int = datetime.now().hour


class ReqBase(SQLModel):
    region: str
    phrase: str


class Req(ReqBase, table=True):
    id: int = Field(default=None, primary_key=True)


class ReqCreate(ReqBase):
    pass


class StatBase(SQLModel):
    id_req: int
    amount: int
    time_of_req: datetime


class Stat(StatBase, table=True):
    id: int = Field(default=None, primary_key=True)


class StatCreate(StatBase):
    pass
