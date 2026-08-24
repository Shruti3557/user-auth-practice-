import random
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.otp import OTP
from app.models.user import User


def create_otp(db: Session, user: User, purpose: str) -> str:
    otp_code = str(random.randint(10**(settings.otp_length - 1), (10**settings.otp_length) - 1))
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.otp_expire_minutes)

    new_otp = OTP(
        user_id=user.id,
        otp=otp_code,
        purpose=purpose,
        expires_at=expires_at,
    )
    db.add(new_otp)
    db.commit()

    print(f"[DEV ONLY] OTP for {user.email}: {otp_code}")
    return otp_code

def verify_otp(db: Session, user: User, otp_input: str, purpose: str) -> bool:
    otp_record = (
        db.query(OTP)
        .filter(OTP.user_id == user.id, OTP.purpose == purpose, OTP.is_verified == False)
        .order_by(OTP.created_at.desc())
        .first()
    )

    if not otp_record:
        return False

    if otp_record.expires_at < datetime.now(timezone.utc):
        return False

    if otp_record.otp != otp_input:
        return False

    otp_record.is_verified = True
    db.commit()
    return True