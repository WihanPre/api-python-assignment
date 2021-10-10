from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from redis import Redis
from sqlalchemy.orm import Session

from app.api import crud, models, schemas
from app.database import SessionLocal, engine

# Uncomment the line below to let the ORM generate tables and relationships for us - if not using migrations
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# DB Dependency
def get_db(request: Request):
    return request.state.db

# health checker
@app.get("/health")
async def root():
    return {"message": "I am healthy, now what"}

# Basic crud operations
@app.post("/appointments/{patient_id}/patients/", response_model=schemas.Appointment)
async def create_appointment(id: int, patient_id: int, appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_patient_appointment(db=db, appointment=appointment, id=id, patient_id=patient_id)

@app.post("/patients/", response_model=schemas.Patient)
async def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = crud.get_patient_by_name(db, name=patient.name)
    if db_patient:
        raise HTTPException (status_code=400, detail="Patient already registered")  #lookup raise
    return crud.create_patient(db=db, patient=patient)

@app.get("/appointments/", response_model=List[schemas.Appointment])
async def get_appointments(skip: int = 0, limit: int = 200, db: Session = Depends(get_db)):
    appointments = crud.get_appointments(db=db, skip=skip, limit=limit)
    return appointments

@app.get("/appointments/{id}", response_model=schemas.Appointment)
async def get_appointmet_id(id: int, db: Session = Depends(get_db)):
    appointment = crud.get_appointment_by_id(db, id=id)
    if appointment is None:
        raise HTTPException (status_code=404, detail="Appointment does not exist")  #lookup raise
    return appointment

@app.delete("/appointments/{id}", status_code=200)
async def delete_appointement_by_id(id: int, db: Session = Depends(get_db)):
    db_appointment = crud.get_appointment_by_id(db, id)
    if db_appointment is None:
        raise HTTPException (status_code=404, detail="Appointment does not exist")  #lookup raise
    return crud.delete_patient_appointment(db, id)

# @app.put("/appointment/{id}", response_model=schemas.Brewer)
