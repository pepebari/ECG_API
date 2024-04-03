from sqlalchemy.orm import Session

from . import models, schemas, security


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def upload_ecg(db: Session, user_id: int, ecg: schemas.ECG):
    db_ecg = models.ECG(user_id=user_id, date=ecg.date)
    db.add(db_ecg)
    db.commit()
    for lead in ecg.leads:
        for idx, value in enumerate(lead.signal):
            db_lead = models.ECGLeads(ecg_id=db_ecg.id, name=lead.name, sample_number=idx+1, voltage_measurement=value)
            db.add(db_lead)
    db.commit()
    db.refresh(db_ecg)
    return ecg


def get_user_ecgs(db: Session, user_id: int):
    userECGs = db.query(models.ECG).filter(models.ECG.user_id == user_id).all()
    return {ecg.id: _convert_ecg_to_base_model(ecg) for ecg in userECGs}


def _convert_ecg_to_base_model(db_ecg: models.ECG) -> schemas.ECG:
    lead_list = []
    lead_names = set([lead.name for lead in db_ecg.leads])
    for lead_name in lead_names:
        leads = [lead for lead in db_ecg.leads if lead.name == lead_name]
        leads = sorted(leads, key=lambda lead: lead.sample_number)
        signal = [lead.voltage_measurement for lead in leads]
        lead_list.append(schemas.ECGLead(name=lead_name, signal=signal, samples=len(signal)))
    return schemas.ECG(date=db_ecg.date, leads=lead_list)
