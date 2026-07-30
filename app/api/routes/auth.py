from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.auth_service import authenticate_user
from app.api.dependencies import get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate a user and return a JWT access token.
    """

    token = authenticate_user(
        username=form_data.username,
        password=form_data.password,
    )

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    """
    Return details of the currently authenticated user.
    """

    return {
        "username": current_user["username"],
        "role": current_user["role"],
    }