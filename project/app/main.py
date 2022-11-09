from fastapi import Depends, FastAPI, Body, BackgroundTasks
from sqlalchemy import select
from sqlmodel import Session
import asyncio


from app.db import get_session, init_db
from app.models import Req, ReqCreate, Stat, StatCreate, DateTime
from app.parsing import get_amount
from datetime import datetime

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/pdfkgpkf")
async def start_collecting_stat(session: Session = Depends(get_session)):
    for i in range(5):
        result = session.execute(select(Req))
        ids = result.scalars().all()
        for id_req in ids:
            amount = get_amount(id_req.phrase)
            st = Stat(id_req=id_req.id, amount=amount, time_of_req=datetime.now())
            session.add(st)
            session.commit()
            session.refresh(st)
        await asyncio.sleep(5)


@app.post("/add")
def add_req(req: ReqCreate, session: Session = Depends(get_session)):
    result = session.execute(select(Req).where(Req.region == req.region).where(Req.phrase == req.phrase))
    request = result.scalars().all()
    if not request:
        req = Req(region=req.region, phrase=req.phrase)
        session.add(req)
        session.commit()
        session.refresh(req)
        amount = get_amount(req.phrase)
        st = Stat(id_req=req.id, amount=amount, time_of_req=datetime.now())
        session.add(st)
        session.commit()
        session.refresh(st)
    else:
        req = request[0]
    return req.id


@app.post("/stat")
def get_stat(from_date: DateTime, to_date: DateTime, id_req: int = Body(...), session: Session = Depends(get_session)):
    to_date = datetime(to_date.year, to_date.month, to_date.day, to_date.hour)
    from_date = datetime(from_date.year, from_date.month, from_date.day, from_date.hour)
    result = session.execute(
        select(Stat).where(Stat.id_req == id_req).where(Stat.time_of_req < to_date).where(Stat.time_of_req > from_date))
    stats = result.scalars().all()
    return [StatCreate(id_req=st.id_req, amount=st.amount, time_of_req=st.time_of_req.isoformat(timespec='minutes')) for
            st in stats]



@app.post("/show_stat")
def show_stat(session: Session = Depends(get_session)):
    result = session.execute(select(Stat))
    stats = result.scalars().all()
    return [StatCreate(id_req=st.id_req, amount=st.amount, time_of_req=st.time_of_req.isoformat(timespec='seconds')) for
            st in stats]


@app.post("/show_req")
def show_req(session: Session = Depends(get_session)):
    result = session.execute(select(Req))
    stats = result.scalars().all()
    return stats

