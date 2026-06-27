import json
import csv
import logging
from typing import List, Dict, Tuple, Any
from agents.card_registry import CardRegistry
from factory.data_alignment_helpers import apply_symmetry_augmentation, normalize_action
from factory.state_dimensions import (
    MAX_BOARD,
    MAX_HAND,
    MAX_OPP_VISIBLE,
    MAX_PRIZES,
    META_FEATURES,
    SINGLE_STATE_DIM,
    STACK_SIZE,
    STATE_DIM,
)

logger = logging.getLogger(__name__)

class DataAligner:
    """Normalizes tournament CSVs and game replays into fixed-size tensors."""
    def __init__(self, card_registry: CardRegistry = None):
        self.registry = card_registry or CardRegistry()
        
        self.MAX_HAND = MAX_HAND
        self.MAX_BOARD = MAX_BOARD
        self.MAX_PRIZES = MAX_PRIZES
        self.MAX_OPP_VISIBLE = MAX_OPP_VISIBLE
        self.META_FEATURES = META_FEATURES
        self.SINGLE_STATE_DIM = SINGLE_STATE_DIM
        self.STACK_SIZE = STACK_SIZE
        self.STATE_DIM = STATE_DIM
        
        self.ACTION_SPACE_OFFSET_PLAY = 0
        self.ACTION_SPACE_OFFSET_ATTACK = 1000
        self.ACTION_SPACE_OFFSET_OTHER = 2000

    def normalize_state(self, raw_state: Dict[str, Any]) -> List[float]:
        """Converts raw game state dict into fixed-size feature tensor."""
        tensor = [0.0] * self.STATE_DIM
        idx = 0
        
        hand = raw_state.get("hand", [])
        for i in range(self.MAX_HAND):
            if i < len(hand): tensor[idx] = float(hand[i])
            idx += 1
            
        active = raw_state.get("active", -1)
        if active != -1: tensor[idx] = float(active)
        idx += 1
        
        bench = raw_state.get("bench", [])
        for i in range(self.MAX_BOARD - 1):
            if i < len(bench): tensor[idx] = float(bench[i])
            idx += 1
            
        prizes = raw_state.get("prize", [])
        for i in range(self.MAX_PRIZES):
            if i < len(prizes): tensor[idx] = 1.0
            idx += 1
            
        opp_visible = raw_state.get("opponent_visible", [])
        for i in range(self.MAX_OPP_VISIBLE):
            if i < len(opp_visible): tensor[idx] = float(opp_visible[i])
            idx += 1
            
        tensor[idx:idx+5] = [
            float(raw_state.get("turn", 0)),
            float(raw_state.get("is_first_player", 0)),
            float(len(hand)), float(len(bench)), float(len(prizes))
        ]
        return tensor

    def apply_symmetry_augmentation(self, state_tensor: List[float]) -> List[float]:
        return apply_symmetry_augmentation(state_tensor, self.STACK_SIZE, self.SINGLE_STATE_DIM, self.MAX_HAND, self.MAX_BOARD)

    def normalize_action(self, raw_action: str) -> int:
        return normalize_action(raw_action, self.ACTION_SPACE_OFFSET_PLAY, self.ACTION_SPACE_OFFSET_ATTACK, self.ACTION_SPACE_OFFSET_OTHER)

    def parse_tournament_csv(self, path: str) -> List[Dict]:
        from factory.data_alignment_normalizer import parse_tournament_csv
        return parse_tournament_csv(path)

    def parse_replay_json(self, path: str) -> List[Dict]:
        from factory.data_alignment_normalizer import parse_replay_json
        return parse_replay_json(path)

    def build_training_dataset(self, source_paths: List[str]) -> Tuple[List[List[float]], List[int]]:
        from factory.data_alignment_normalizer import build_training_dataset
        return build_training_dataset(self, source_paths)
