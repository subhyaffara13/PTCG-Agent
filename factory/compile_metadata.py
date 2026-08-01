import json
import csv
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from utils.compile_metadata import compile_metadata

if __name__ == "__main__":
    compile_metadata()
