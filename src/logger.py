import logging
from pathlib import Path


# ============================================================
# LOG DIRECTORY
# ============================================================

LOG_DIRECTORY = Path("data/logs")

LOG_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOG FILE
# ============================================================

LOG_FILE = LOG_DIRECTORY / "pipeline.log"


# ============================================================
# LOGGER CONFIGURATION
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_FILE,
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)


# ============================================================
# PROJECT LOGGER
# ============================================================

logger = logging.getLogger(
    "voice_mom_pipeline"
)


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    logger.info(
        "Voice-Based Minutes of Meeting logging system started."
    )

    logger.info(
        "Logger test completed successfully."
    )

    print(
        f"\nLog file created at: {LOG_FILE}"
    )