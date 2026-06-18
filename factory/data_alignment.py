import json
import csv
import logging
from typing import List, Dict, Tuple, Any
from agents.card_registry import CardRegistry

logger = logging.getLogger(__name__)

class DataAligner:
    """
    Normalizes external tournament CSVs and game replay JSONs into fixed-size feature tensors.
    
    Converts variable-length game states (hands, benches, prizes) into a fixed dimension
    suitable for neural networks. It also supports Frame Stacking (giving the agent temporal
    memory of previous turns) and Symmetry Augmentation (shuffling bench slots to multiply
    training data without running new simulations).
    """
    def __init__(self, card_registry: CardRegistry = None):
        self.registry = card_registry or CardRegistry()
        
        # State tensor size:
        # Hand (20 max) + Board (20 max) + Prizes (6) + Opponent Visible (20 max) + Turn/Phase (5)
        self.MAX_HAND = 20
        self.MAX_BOARD = 20
        self.MAX_PRIZES = 6
        self.MAX_OPP_VISIBLE = 20
        self.META_FEATURES = 5
        self.SINGLE_STATE_DIM = self.MAX_HAND + self.MAX_BOARD + self.MAX_PRIZES + self.MAX_OPP_VISIBLE + self.META_FEATURES
        
        self.STACK_SIZE = 3 # Current turn + 2 previous turns
        self.STATE_DIM = self.SINGLE_STATE_DIM * self.STACK_SIZE
        
        # Action space definition
        # Very simplified for this module's scope: 0-999 = card IDs to play, 1000-1999 = attacks, etc.
        self.ACTION_SPACE_OFFSET_PLAY = 0
        self.ACTION_SPACE_OFFSET_ATTACK = 1000
        self.ACTION_SPACE_OFFSET_OTHER = 2000

    def normalize_state(self, raw_state: Dict[str, Any]) -> List[float]:
        """Converts raw game state dict into fixed-size feature tensor."""
        tensor = [0.0] * self.STATE_DIM
        idx = 0
        
        # Hand (pad or truncate to MAX_HAND)
        hand = raw_state.get("hand", [])
        for i in range(self.MAX_HAND):
            if i < len(hand):
                tensor[idx] = float(hand[i])
            idx += 1
            
        # Board (active + bench)
        active = raw_state.get("active", -1)
        if active != -1:
            tensor[idx] = float(active)
        idx += 1
        
        bench = raw_state.get("bench", [])
        for i in range(self.MAX_BOARD - 1):
            if i < len(bench):
                tensor[idx] = float(bench[i])
            idx += 1
            
        # Prizes
        prizes = raw_state.get("prize", [])
        for i in range(self.MAX_PRIZES):
            if i < len(prizes):
                tensor[idx] = 1.0  # Just indicating presence, not identity
            idx += 1
            
        # Opponent visible (their active + bench)
        opp_visible = raw_state.get("opponent_visible", [])
        for i in range(self.MAX_OPP_VISIBLE):
            if i < len(opp_visible):
                tensor[idx] = float(opp_visible[i])
            idx += 1
            
        # Meta features
        tensor[idx] = float(raw_state.get("turn", 0))
        tensor[idx+1] = float(raw_state.get("is_first_player", 0))
        tensor[idx+2] = float(len(hand))
        tensor[idx+3] = float(len(bench))
        tensor[idx+4] = float(len(prizes))
        
        return tensor

    def apply_symmetry_augmentation(self, state_tensor: List[float]) -> List[float]:
        """
        Data Augmentation: Shuffles the bench pokemon in the state tensor.
        Since bench order doesn't matter, this creates valid synthetic training data.
        """
        import random
        new_tensor = list(state_tensor)
        
        for frame in range(self.STACK_SIZE):
            offset = frame * self.SINGLE_STATE_DIM
            bench_start = offset + self.MAX_HAND + 1
            bench_end = bench_start + (self.MAX_BOARD - 1)
            
            # Extract bench slice, shuffle non-zero elements
            bench_slice = new_tensor[bench_start:bench_end]
            active_elements = [x for x in bench_slice if x != 0.0]
            zeros = [0.0] * (len(bench_slice) - len(active_elements))
            
            random.shuffle(active_elements)
            new_bench = active_elements + zeros
            
            # Put back
            new_tensor[bench_start:bench_end] = new_bench
            
        return new_tensor

    def normalize_action(self, raw_action: str) -> int:
        """Maps action string to integer action ID."""
        if not raw_action:
            return self.ACTION_SPACE_OFFSET_OTHER + 999  # Pass
            
        if raw_action.startswith("attack:"):
            # Simplified: just hash the attack name or map to a fixed range
            return self.ACTION_SPACE_OFFSET_ATTACK + (hash(raw_action) % 1000)
            
        if raw_action.startswith("play:"):
            try:
                card_id = int(raw_action.split(":")[1])
                return self.ACTION_SPACE_OFFSET_PLAY + card_id
            except:
                pass
                
        return self.ACTION_SPACE_OFFSET_OTHER + 1

    def parse_tournament_csv(self, path: str) -> List[Dict]:
        """Parse pro match logs in CSV format."""
        samples = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Implement actual parsing logic based on CSV schema
                    # This is placeholder conversion
                    state = {"turn": int(row.get("Turn", 0))}
                    action = row.get("Action", "pass")
                    reward = 1.0 if row.get("Won") == "True" else 0.0
                    samples.append({"state": state, "action": action, "reward": reward})
        except Exception as e:
            logger.error(f"Failed to parse CSV {path}: {e}")
        return samples

    def parse_replay_json(self, path: str) -> List[Dict]:
        """Parse game replay JSON."""
        samples = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for step in data.get("steps", []):
                    # Placeholder for actual JSON replay schema
                    state = step.get("state", {})
                    action = step.get("action", "pass")
                    reward = step.get("reward", 0.0)
                    samples.append({"state": state, "action": action, "reward": reward})
        except Exception as e:
            logger.error(f"Failed to parse JSON {path}: {e}")
        return samples

    def build_training_dataset(self, source_paths: List[str]) -> Tuple[List[List[float]], List[int]]:
        """Builds tensors ready for model training, applying frame stacking and augmentation."""
        states = []
        actions = []
        
        for path in source_paths:
            samples = []
            if path.endswith(".csv"):
                samples = self.parse_tournament_csv(path)
            elif path.endswith(".json"):
                samples = self.parse_replay_json(path)
                
            # Frame stacking queue
            from collections import deque
            frame_stack = deque([[0.0] * self.SINGLE_STATE_DIM] * self.STACK_SIZE, maxlen=self.STACK_SIZE)
            
            for s in samples:
                try:
                    norm_single_state = self.normalize_state(s["state"])
                    frame_stack.append(norm_single_state)
                    
                    # Flatten the frame stack into a single tensor
                    stacked_tensor = []
                    for frame in frame_stack:
                        stacked_tensor.extend(frame)
                        
                    norm_action = self.normalize_action(s["action"])
                    
                    # Original sample
                    states.append(stacked_tensor)
                    actions.append(norm_action)
                    
                    # Augmentation (create 2 additional synthetic samples via symmetry)
                    for _ in range(2):
                        aug_tensor = self.apply_symmetry_augmentation(stacked_tensor)
                        states.append(aug_tensor)
                        actions.append(norm_action)
                        
                except Exception as e:
                    logger.warning(f"Skipping malformed sample: {e}")
                    
        return states, actions
