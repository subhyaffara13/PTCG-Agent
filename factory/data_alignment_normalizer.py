import json
import csv
import logging
from collections import deque
from typing import List, Dict, Tuple, Any

logger = logging.getLogger("DataAlignmentNormalizer")

def parse_tournament_csv(path: str) -> List[Dict]:
    """Parse pro match logs in CSV format."""
    samples = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                state = {"turn": int(row.get("Turn", 0))}
                action = row.get("Action", "pass")
                reward = 1.0 if row.get("Won") == "True" else 0.0
                samples.append({"state": state, "action": action, "reward": reward})
    except Exception as e:
        logger.error(f"Failed to parse CSV {path}: {e}")
    return samples

def parse_replay_json(path: str) -> List[Dict]:
    """Parse game replay JSON."""
    samples = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for step in data.get("steps", []):
                state = step.get("state", {})
                action = step.get("action", "pass")
                reward = step.get("reward", 0.0)
                samples.append({"state": state, "action": action, "reward": reward})
    except Exception as e:
        logger.error(f"Failed to parse JSON {path}: {e}")
    return samples

def build_training_dataset(aligner, source_paths: List[str]) -> Tuple[List[List[float]], List[int]]:
    """Builds tensors ready for model training, applying frame stacking and augmentation."""
    states = []
    actions = []
    
    for path in source_paths:
        samples = []
        if path.endswith(".csv"):
            samples = parse_tournament_csv(path)
        elif path.endswith(".json"):
            samples = parse_replay_json(path)
            
        frame_stack = deque([[0.0] * aligner.SINGLE_STATE_DIM] * aligner.STACK_SIZE, maxlen=aligner.STACK_SIZE)
        
        for s in samples:
            try:
                norm_single_state = aligner.normalize_state(s["state"])
                frame_stack.append(norm_single_state)
                
                stacked_tensor = []
                for frame in frame_stack:
                    stacked_tensor.extend(frame)
                    
                norm_action = aligner.normalize_action(s["action"])
                
                states.append(stacked_tensor)
                actions.append(norm_action)
                
                for _ in range(2):
                    aug_tensor = aligner.apply_symmetry_augmentation(stacked_tensor)
                    states.append(aug_tensor)
                    actions.append(norm_action)
                    
            except Exception as e:
                logger.warning(f"Skipping malformed sample: {e}")
                
    return states, actions
