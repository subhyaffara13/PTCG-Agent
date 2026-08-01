import csv
import logging
from pathlib import Path
logger = logging.getLogger("QATeam")

from utils.parse_deck_csv import parse_deck_csv

from utils.validate_candidates import validate_candidates
