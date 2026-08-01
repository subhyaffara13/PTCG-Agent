import os
import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

_DYNAMIC_PREFERENCE_MAP = None
ENERGY_PREFERENCE_MAP = {
    "957": "6", "87": "6", "734": "6", "733": "6", "950": "6",
    "979": "6", "226": "6", "855": "2", "37": "4",
    "62": "6",
    "63": "4",
    "231": "3"
}

from utils._initialize_preference_map import _initialize_preference_map
