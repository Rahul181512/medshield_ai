from fastapi import APIRouter, HTTPException

from app.auth.users import FAKE_USERS

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/")
def get_users():
    """
    Return all registered users.
    """

    return [
        {
            "username": user["username"],
            "role": user["role"],
        }
        for user in FAKE_USERS.values()
    ]


@router.get("/{username}")
def get_user_details(username: str):
    """
    Return details of a specific user.
    """

    user = FAKE_USERS.get(username)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found.",
        )

    return {
        "username": user["username"],
        "role": user["role"],
    }