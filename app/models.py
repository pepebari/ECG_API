from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    role = Column(String, default="USER")
    hashed_password = Column(String)

    ecgs = relationship("ECG", back_populates="user")


class ECG(Base):
    __tablename__ = "ecg"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(DateTime)

    user = relationship("User", back_populates="ecgs")

    leads= relationship("ECGLeads", back_populates="recording")


class ECGLeads(Base):
    __tablename__ = 'ecg_leads'

    id = Column(Integer, primary_key=True)
    ecg_id = Column(Integer, ForeignKey('ecg.id'))
    name = Column(String)
    sample_number = Column(Integer)
    voltage_measurement = Column(Integer)

    recording = relationship("ECG", back_populates="leads")
