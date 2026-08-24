from fastapi import FastAPI 
from pydantic import BaseModel
from typing import Optional, Generic, TypeVar
from app.core.database import Base, engine
from app.api.routes import auth
from app.models import otp
from app.api.routes import otp
from app.api.routes import profile
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

T=TypeVar("T")

class ErrorDetail(BaseModel):
    code: int
    msg: str

class APIResponse(BaseModel, Generic[T]):
    status: bool
    data: Optional[T]= None 
    error: Optional[ErrorDetail]= None

app=FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(auth.router)
app.include_router(otp.router)
app.include_router(profile.router)
users_db=[]

class User(BaseModel):
    name: str
    email: str

@app.post("/users/")
def create_user(user: User):
    users_db.append(user)
    return APIResponse(status=True, data=user, error=None)


@app.get("/")
async def root():
    return {"message": "Hello, my API is working!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/greet")
def greet(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/greet/{name}")
def greet_path(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/users/")
def get_users():
    return users_db

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": False, "data": None, "error": {"code": exc.status_code, "msg": str(exc.detail)}},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    return JSONResponse(
        status_code=422,
        content={"status": False, "data": None, "error": {"code": 422, "msg": first_error.get("msg", "Validation error")}},
    )
