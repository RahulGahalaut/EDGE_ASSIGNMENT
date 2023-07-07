from sqlalchemy import Column, Integer, String, DateTime
from database import Base


# Model for the source data
class SourceData(Base):
    __tablename__ = 'source_data'

    source_id = Column(Integer, primary_key=True)
    source = Column(String(200))
    source_type = Column(String(10))
    source_tag = Column(String(10))
    last_update_date = Column(DateTime)
    from_date = Column(DateTime)
    to_date = Column(DateTime)
    frequency = Column(String(5), default="15M")
