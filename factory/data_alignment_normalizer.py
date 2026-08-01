import json
import csv
import logging
from collections import deque
from typing import List, Dict, Tuple, Any

logger = logging.getLogger("DataAlignmentNormalizer")

from utils.parse_tournament_csv import parse_tournament_csv

from utils.parse_replay_json import parse_replay_json

from utils.build_training_dataset import build_training_dataset
