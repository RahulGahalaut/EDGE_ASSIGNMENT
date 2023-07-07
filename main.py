from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from models import SourceData
from database import engine, SessionLocal, Base
import logging
from sqlalchemy.exc import SQLAlchemyError

# Initialize FastAPI app
app = FastAPI()

# Create the database tables
Base.metadata.create_all(bind=engine)


# Model for the request payload for add_data
class SourceDataPayload(BaseModel):
    source: str
    source_type: str
    source_tag: str
    last_update_date: datetime
    from_date: datetime
    to_date: datetime
    frequency: str


# Model for the request payload for update_data
class SourceDataUpdatePayload(BaseModel):
    last_update_date: datetime
    from_date: datetime
    to_date: datetime


# Logger configuration
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


@app.get('/get_data')
def get_data(source_id: int):
    try:
        session = SessionLocal()
        source_data = session.query(SourceData).filter(
            SourceData.source_id == source_id).first()
        session.close()

        if source_data:
            return source_data.__dict__
        else:
            raise HTTPException(
                status_code=404, detail="Source data not found")

    except SQLAlchemyError as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get('/get_data_trigger')
def get_data_trigger(source_id: int):
    try:
        session = SessionLocal()
        source_data = session.query(SourceData).filter(
            SourceData.source_id == source_id).first()

        if source_data:
            updated_dates = {
                'from_date': source_data.from_date + timedelta(minutes=int(source_data.frequency[:-1])),
                'to_date': source_data.to_date + timedelta(minutes=int(source_data.frequency[:-1]))
            }
            source_data_dict = source_data.__dict__
            source_data_dict.update(updated_dates)
            session.close()
            return source_data_dict
        else:
            session.close()
            raise HTTPException(
                status_code=404, detail="Source data not found")

    except SQLAlchemyError as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@app.patch('/update_data')
def update_data(source_id: int, payload: SourceDataUpdatePayload):
    try:
        session = SessionLocal()
        source_data = session.query(SourceData).filter(
            SourceData.source_id == source_id).first()

        if source_data:
            source_data.from_date = payload.from_date
            source_data.to_date = payload.to_date
            source_data.last_update_date = payload.last_update_date
            session.commit()
            session.close()
            return {"status": "success"}
        else:
            session.close()
            raise HTTPException(
                status_code=404, detail="Source data not found")

    except SQLAlchemyError as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post('/add_data')
def add_data(payload: SourceDataPayload):
    try:
        session = SessionLocal()
        source_data = SourceData(
            source=payload.source,
            source_type=payload.source_type,
            source_tag=payload.source_tag,
            last_update_date=payload.last_update_date,
            from_date=payload.from_date,
            to_date=payload.to_date,
            frequency=payload.frequency
        )
        session.add(source_data)
        session.commit()
        session.close()

        return {"status": "success"}

    except SQLAlchemyError as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="Internal server error")
