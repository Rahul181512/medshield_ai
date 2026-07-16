from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """
    Schema for user login request.
    """

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Username of the user"
    )

    password: str = Field(
        ...,
        min_length=6,
        max_length=72,
        description="User password (bcrypt supports up to 72 bytes)"
    )


class TokenResponse(BaseModel):
    """
    Schema returned after successful authentication.
    """

    access_token: str = Field(
        ...,
        description="JWT access token"
    )

    token_type: str = Field(
        default="bearer",
        description="Authentication token type"
    )


class TokenData(BaseModel):
    """
    Data extracted from a decoded JWT.
    """

    username: str | None = Field(
        default=None,
        description="Authenticated username"
    )