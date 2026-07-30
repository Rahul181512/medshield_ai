from pathlib import Path

from fastapi import APIRouter

router = APIRouter(
    prefix="/audit",
    tags=["Audit"],
)

LOG_FILE = Path("logs/audit.log")


@router.get("/logs")
def get_logs():
    """
    Return the latest audit log entries.
    """

    if not LOG_FILE.exists():
        return {
            "count": 0,
            "logs": [],
        }

    with open(LOG_FILE, "r") as file:
        logs = file.readlines()

    return {
        "count": len(logs),
        "logs": logs[-50:],
    }


@router.get("/stats")
def get_stats():
    """
    Return audit log statistics.
    """

    if not LOG_FILE.exists():
        return {
            "total_logs": 0,
        }

    with open(LOG_FILE, "r") as file:
        logs = file.readlines()

    return {
        "total_logs": len(logs),
    }