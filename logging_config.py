import logging
import os
import pytz
from datetime import datetime

def setup_logging(log_dir: str):
    if not os.path.exists(log_dir):
        try:
            os.makedirs(log_dir)
        except Exception as e:
            print(f"Greška pri kreiranju log direktorijuma: {e}")

    # Timezone
    desired_timezone = pytz.timezone("Europe/Belgrade")

    # Name of logg file
    log_filename = datetime.now(desired_timezone).strftime("%Y-%m-%d_%H-%M-%S") + ".log"
    log_filepath = os.path.join(log_dir, log_filename)

    # Configure logging
    logging.Formatter.converter = lambda *args: datetime.now(desired_timezone).timetuple()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s",
        handlers=[
            logging.FileHandler(log_filepath),
            logging.StreamHandler(),
        ],
    )

    logging.info("Configured logging.")