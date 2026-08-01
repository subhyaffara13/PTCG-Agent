"""
cb_agents/opponent_model_helpers.py

Helper logic for OpponentModel: archetype classification and action predictions.
"""

from __future__ import annotations
from typing import Dict, List, Any


# Map Pokemon IDs to archetypes for fast lookup
KEY_ID_TO_ARCHETYPE = {
    "1092": "setup",
    "721": "aggro",
    "722": "aggro",
    "1145": "stall",
    "1163": "stall",
    "1121": "control",
    "1262": "combo"
}

from utils.identify_opponent_archetype import identify_opponent_archetype

from utils.predict_opponent_action import predict_opponent_action
