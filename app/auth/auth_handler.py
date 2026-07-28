from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): Data to encode inside the JWT payload.

    Returns:
        str: Encoded JWT token.
    """

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def verify_access_token(token: str) -> dict | None:
    """
    Verify and decode a JWT access token.

    Args:
        token (str): JWT token.

    Returns:
        dict | None:
            Decoded payload if valid,
            None if invalid or expired.
    """

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:
        return None