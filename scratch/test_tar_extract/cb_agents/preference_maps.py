"""
cb_agents/preference_maps.py
Contains dynamic energy card preference mappings for optimal Pokemon attachments.
"""
import os
import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Fallback static map if CSV cannot be loaded
ENERGY_PREFERENCE_MAP = {
    "957": "4", "87": "4", "734": "4", "733": "4", "950": "4",
    "979": "6", "226": "6", "855": "2"
}

_DYNAMIC_PREFERENCE_MAP = None

from utils._initialize_preference_map import _initialize_preference_map

from utils.get_energy_preference import get_energy_preference
