from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base  
from models import RawData, Alert               

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Real-Time Backend")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "API is running"}

@app.post("/raw_data/")
def create_raw_data(
    temperature: float,
    humidity: float,
    voltage: float,
    pressure: float,
    light: float,
    db: Session = Depends(get_db)
):
    raw_entry = RawData(
        temperature=temperature,
        humidity=humidity,
        voltage=voltage,
        pressure=pressure,
        light=light,
        raw_json="{}"  
    )
    db.add(raw_entry)
    db.commit()
    db.refresh(raw_entry)
    return raw_entry

@app.get("/raw_data/")
def read_raw_data(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    entries = db.query(RawData).offset(skip).limit(limit).all()
    return entries

@app.post("/alerts/")
def create_alert(
    raw_id: int,
    key: str,
    value: float,
    threshold: float,
    db: Session = Depends(get_db)
):
    alert = Alert(
        raw_id=raw_id,
        key=key,
        value=value,
        threshold=threshold
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

@app.get("/alerts/")
def read_alerts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    alerts = db.query(Alert).offset(skip).limit(limit).all()
    return alerts