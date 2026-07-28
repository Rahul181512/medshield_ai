from app.auth.users import get_user
from app.auth.security import verify_password
from app.auth.auth_handler import create_access_token


def authenticate_user(username: str, password: str):
    """
    Authenticate a user and generate an access token.

    Args:
        username (str): Username entered by the user.
        password (str): Plain text password.

    Returns:
        dict | None:
            JWT token response if authentication succeeds,
            otherwise None.
    """

    user = get_user(username)

    if not user:
        return None

    if not verify_password(password, user["hashed_password"]):
        return None

    access_token = create_access_token(
        {
            "sub": user["username"],
            "role": user["role"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }