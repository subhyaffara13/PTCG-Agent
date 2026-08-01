import os
import json
import tarfile
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("submission_packer")

from utils.generate_description import generate_description

from utils.pack_submission import pack_submission

if __name__ == "__main__":
    pack_submission()
