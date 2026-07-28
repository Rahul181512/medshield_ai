FAKE_USERS = {
    "doctor": {
        "username": "doctor",
        "hashed_password": "$2b$12$ukCLJTBf9QIOvCDf3q1UMuFETosouqXt9erKIdAnfi1cGlOEA3gTe",
        "role": "doctor",
    },
    "compliance_officer": {
        "username": "compliance_officer",
        "hashed_password": "$2b$12$ATjtK4y7.sbygJNbiAOgtesRoJThE3.Yhi2woa6LIhpQ.oCs1.tta",
        "role": "compliance_officer",
    },
    "admin": {
        "username": "admin",
        "hashed_password": "$2b$12$xFKdKMuQCx4ceqKiOCXoGOhMJ6Vlo4VEmFqELZCsejOkw9XHYKQN2",
        "role": "admin",
    },
}


def get_user(username: str):
    """Retrieve a user by username."""
    return FAKE_USERS.get(username)