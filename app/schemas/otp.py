from pydantic import BaseModel, EmailStr


class GenerateOTPRequest(BaseModel):
    email: EmailStr


class GenerateOTPResponse(BaseModel):
    message: str


class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str


class VerifyOTPResponse(BaseModel):
    message: str