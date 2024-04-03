from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from . import crud, schemas, security
from .database import create_database_tables, get_db
from .insights import calculate_insights

create_database_tables()
app = FastAPI()


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
) -> security.Token:
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return security.create_access_token_for_user(user.username)


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, current_user: Annotated[str, Depends(security.get_admin_user)], db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already in use")
    return crud.create_user(db=db, user=user)


@app.post("/ecgs/", response_model=schemas.ECG)
def upload_ecg(ecg: schemas.ECG, current_user: Annotated[str, Depends(security.get_current_user)], db: Session = Depends(get_db)):
    if current_user.role == "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin user cannot upload ecg",
        )
    return crud.upload_ecg(db, user_id=current_user.id, ecg=ecg)


@app.get("/ecgs/{ecg_id}/insights/", response_model=schemas.ECGInsight)
def get_ecg_insights(ecg_id: int, current_user: Annotated[str, Depends(security.get_current_user)], db: Session = Depends(get_db)):
    user_ecgs = crud.get_user_ecgs(db, current_user.id)
    if ecg_id not in user_ecgs:
        raise HTTPException(status_code=404, detail="ECG not found")

    return calculate_insights(user_ecgs[ecg_id])
