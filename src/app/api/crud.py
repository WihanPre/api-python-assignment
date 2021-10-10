from sqlalchemy.orm import Session

from app.main import db_session_middleware
from . import models, schemas

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def get_patient_by_name(db: Session, name: str):
    return db.query(models.Patient).filter(models.Patient.name == name).first()

def get_patient_by_id(db: Session, id: id):
    return db.query(models.Patient).filter(models.Patient.id == id).first()

def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(name=patient.name)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, id: int):
    return db.query(models.Patient).delete(models.Patient.id == id)


def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Appointment).offset(skip).limit(limit).all()

def create_patient_appointment(db: Session, appointment: schemas.AppointmentCreate, id: int, patient_id: int): ##Must be wrong
    db_appointment = models.Appointment(id=id, patient_id=patient_id)  ##Must be wrong
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_appointment_by_id(db: Session, id: int):
    return db.query(models.Appointment).filter(models.Appointment.id == id)

def delete_patient_appointment(db: Session, id: int):
    return db.query(models.Appointment).delete(models.Appointment.id == id)
