from fastapi import APIRouter, HTTPException, status

from app.schemas.auth_schema import LoginRequest
from app.auth.auth_service import authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(login_data: LoginRequest):
    """
    Authenticate user and return a JWT access token.
    """

    token = authenticate_user(
        username=login_data.username,
        password=login_data.password
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password."
        )

    return token