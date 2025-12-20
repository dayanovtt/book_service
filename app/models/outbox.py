from sqlalchemy import Column, Integer, String, DateTime, JSON, func

from app.db.session import Base


class Outbox(Base):
    __tablename__ = "outbox"

    id = Column(Integer, primary_key=True)
    event_type = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
