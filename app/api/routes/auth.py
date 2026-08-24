from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import (
    LoginRequest,
    LogoutRequest,
    LogoutResponse,
    SignupRequest,
    SignupResponse,
    TokenResponse,
)
from app.schemas.common import APIResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=APIResponse[SignupResponse])
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    try:
        user = auth_service.signup_user(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    data = SignupResponse(message="Signup successful", email=user.email)
    return APIResponse(status=True, data=data, error=None)


@router.post("/login", response_model=APIResponse[TokenResponse])
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    try:
        user = auth_service.authenticate_user(db, payload.email, payload.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    access_token = auth_service.create_access_token(user.id)
    refresh_token = auth_service.create_refresh_token(db, user)

    data = TokenResponse(access_token=access_token, refresh_token=refresh_token)
    return APIResponse(status=True, data=data, error=None)


@router.post("/logout", response_model=APIResponse[LogoutResponse])
def logout(payload: LogoutRequest, db: Session = Depends(get_db)):
    try:
        auth_service.revoke_refresh_token(db, payload.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    data = LogoutResponse(message="Logged out successfully")
    return APIResponse(status=True, data=data, error=None)