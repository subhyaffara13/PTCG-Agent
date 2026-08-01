"""
cb_agents/preference_maps.py
Contains dynamic energy card preference mappings for optimal Pokemon attachments.
"""
import os
import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

ENERGY_PREFERENCE_MAP = {
    "957": "6", "87": "6", "734": "6", "733": "6", "950": "6",
    "979": "6", "226": "6", "855": "2", "37": "4",
    "62": "6",   # Koraidon (Fighting '6')
    "63": "4",   # Raging Bolt ex (Lightning '4')
    "231": "3"   # Tatsugiri ex (Water '3')
}

_DYNAMIC_PREFERENCE_MAP = None

from utils._initialize_preference_map import _initialize_preference_map

from utils.get_energy_preference import get_energy_preference
