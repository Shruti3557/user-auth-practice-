from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings
from passlib.context import CryptContext
from jose import JWTError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.auth import SignupRequest
from app.services.user_service import get_user_by_email


def signup_user(db: Session, payload: SignupRequest) -> User:
    existing_user = get_user_by_email(db, payload.email)
    if existing_user:
        raise ValueError("Email already registered")

    new_user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        first_name=payload.first_name,
        last_name=payload.last_name,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = get_user_by_email(db, email)
    if not user:
        raise ValueError("Invalid email or password")

    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid email or password")

    return user
import uuid


def create_refresh_token(db: Session, user: User) -> str:
    jti = str(uuid.uuid4())
    user.current_refresh_jti = jti
    db.commit()

    expire = datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
    payload = {"sub": str(user.id), "jti": jti, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def revoke_refresh_token(db: Session, refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    except JWTError:
        raise ValueError("Invalid token")

    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()

    if user:
        user.current_refresh_jti = None
        db.commit()