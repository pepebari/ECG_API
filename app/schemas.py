from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Literal
from datetime import datetime


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Literal["USER", "ADMIN"]

class UserInDB(User):
    hashed_password: str

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal["USER", "ADMIN"]

class ECGLead(BaseModel):
    name: str
    samples: Optional[int] = None
    signal: List[int]

class ECG(BaseModel):
    date: datetime
    leads: List[ECGLead]

class ECGInsight(BaseModel):
    zero_crossings: Dict[str, int]
