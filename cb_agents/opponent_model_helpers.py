"""
cb_agents/opponent_model_helpers.py

Helper logic for OpponentModel: archetype classification and action predictions.
"""

from __future__ import annotations
from typing import Dict, List, Any


# Map known competitive Pokemon IDs to archetypes for fast lookup
KEY_ID_TO_ARCHETYPE = {
    "721": "aggro",
    "722": "aggro",
    "979": "aggro",
    "1145": "stall",
    "1163": "stall",
    "1121": "control",
    "1262": "combo",
    "1260": "combo",
}

from cb_agents.card_registry import CardRegistry
_registry = None

from utils.get_card_identifier import get_card_identifier

from utils.identify_opponent_archetype import identify_opponent_archetype

from utils.predict_opponent_action import predict_opponent_action
