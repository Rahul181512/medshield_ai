from datetime import datetime
from pathlib import Path


# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "audit.log"


def log_redaction(
    username: str,
    entities: list,
    status: str = "SUCCESS",
):
    """
    Log every redaction request to audit.log
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    entity_names = ", ".join(
        entity.type for entity in entities
    )

    log_entry = (
        f"[{timestamp}] "
        f"User={username} | "
        f"Entities={entity_names if entity_names else 'None'} | "
        f"Status={status}\n"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(log_entry)