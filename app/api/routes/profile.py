from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.user import UserResponse

router = APIRouter(tags=["profile"])


@router.get("/profile", response_model=APIResponse[UserResponse])
def get_profile(current_user: User = Depends(get_current_user)):
    data = UserResponse.model_validate(current_user)
    return APIResponse(status=True, data=data, error=None)