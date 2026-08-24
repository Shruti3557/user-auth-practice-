from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.common import APIResponse
from app.schemas.otp import (
    GenerateOTPRequest,
    GenerateOTPResponse,
    VerifyOTPRequest,
    VerifyOTPResponse,
)
from app.services import otp_service, user_service

router = APIRouter(prefix="/auth", tags=["otp"])


@router.post("/generate-otp", response_model=APIResponse[GenerateOTPResponse])
def generate_otp(payload: GenerateOTPRequest, db: Session = Depends(get_db)):
    user = user_service.get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    purpose = "login" if user.is_verified else "signup"
    otp_service.create_otp(db, user, purpose)

    data = GenerateOTPResponse(message="OTP sent successfully")
    return APIResponse(status=True, data=data, error=None)


@router.post("/verify-otp", response_model=APIResponse[VerifyOTPResponse])
def verify_otp(payload: VerifyOTPRequest, db: Session = Depends(get_db)):
    user = user_service.get_user_by_email(db, payload.email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    purpose = "signup" if not user.is_verified else "login"
    is_valid = otp_service.verify_otp(db, user, payload.otp, purpose)

    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    if purpose == "signup":
        user_service.mark_user_verified(db, user)

    data = VerifyOTPResponse(message="OTP verified successfully")
    return APIResponse(status=True, data=data, error=None)