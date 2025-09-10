from models import RawData, Alert
from database import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import json

def store_raw_data(data_dict):
    """
    Stores the full sensor data payload into the raw_data table.
    Expects keys: temperature, humidity, voltage, pressure, light
    Returns inserted row id or None on failure.
    """
    db = SessionLocal()
    try:
        db_data = RawData(
            temperature=_safe_float(data_dict.get("temperature")),
            humidity=_safe_float(data_dict.get("humidity")),
            voltage=_safe_float(data_dict.get("voltage")),
            pressure=_safe_float(data_dict.get("pressure")),
            light=_safe_float(data_dict.get("light")),
            raw_json=json.dumps(data_dict),
            timestamp=datetime.utcnow()
        )
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        return db_data.id
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[crud] Error storing raw data: {e}")
        return None
    finally:
        db.close()

def store_alert(raw_id, key, value, threshold):
    """
    Stores an alert into the alerts table.
    """
    db = SessionLocal()
    try:
        alert = Alert(
            raw_id=raw_id,
            key=key,
            value=value,
            threshold=threshold,
            timestamp=datetime.utcnow()
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        print(f"[crud] Alert stored: raw_id={raw_id} {key}={value} exceeded {threshold}")
        return alert.id
    except SQLAlchemyError as e:
        db.rollback()
        print(f"[crud] Error storing alert: {e}")
        return None
    finally:
        db.close()

def get_raw_data(limit: int = 100):
    db = SessionLocal()
    try:
        return db.query(RawData).order_by(RawData.timestamp.desc()).limit(limit).all()
    finally:
        db.close()

def get_alert_data(limit: int = 100):
    db = SessionLocal()
    try:
        return db.query(Alert).order_by(Alert.timestamp.desc()).limit(limit).all()
    finally:
        db.close()

def _safe_float(value):
    try:
        return float(value) if value is not None else None
    except (ValueError, TypeError):
        return None
