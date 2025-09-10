from sqlalchemy import Column, Integer, Float, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class RawData(Base):
    __tablename__ = "raw_data"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    voltage = Column(Float, nullable=True)
    pressure = Column(Float, nullable=True)
    light = Column(Float, nullable=True)
    raw_json = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    
    alerts = relationship("Alert", back_populates="raw_data", cascade="all, delete-orphan")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    raw_id = Column(Integer, ForeignKey("raw_data.id", ondelete="CASCADE"), nullable=False)
    key = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    threshold = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    
    raw_data = relationship("RawData", back_populates="alerts")
