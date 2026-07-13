import hashlib
import random
from typing import List

def _deterministic_hash(s: str) -> int:
    return int(hashlib.md5(s.encode()).hexdigest(), 16)

def apply_symmetry_augmentation(state_tensor: List[float], stack_size: int, single_state_dim: int, max_hand: int, max_board: int) -> List[float]:
    """
    Data Augmentation: Shuffles the bench pokemon in the state tensor.
    """
    new_tensor = list(state_tensor)
    for frame in range(stack_size):
        offset = frame * single_state_dim
        bench_start = offset + max_hand + 1
        bench_end = bench_start + (max_board - 1)

        bench_slice = new_tensor[bench_start:bench_end]
        active_elements = [x for x in bench_slice if x != 0.0]
        zeros = [0.0] * (len(bench_slice) - len(active_elements))

        random.shuffle(active_elements)
        new_bench = active_elements + zeros

        new_tensor[bench_start:bench_end] = new_bench

    return new_tensor

def normalize_action(raw_action: str, offset_play: int, offset_attack: int, offset_other: int) -> int:
    """Maps action string to an integer action ID with deterministic structured encoding."""
    if not raw_action:
        return offset_other + 999  # Pass

    if raw_action.startswith("attack:"):
        return offset_attack + (_deterministic_hash(raw_action) % 1000)

    if raw_action.startswith("play_trainer:"):
        tn = raw_action.split(":", 1)[1]
        return offset_play + (_deterministic_hash(tn) % 1000)

    if raw_action.startswith("retreat:"):
        parts = raw_action.split(":")
        if len(parts) >= 2 and parts[1].lstrip("-").isdigit():
            return offset_play + (int(parts[1]) % 1000)
        return offset_play + (_deterministic_hash(raw_action) % 1000)

    if raw_action.startswith("play:") or raw_action.startswith("bench:") or raw_action.startswith("evolve:") or raw_action.startswith("attach_energy:") or raw_action.startswith("ability:"):
        parts = raw_action.split(":")
        if len(parts) >= 2 and parts[1].lstrip("-").isdigit():
            return offset_play + (int(parts[1]) % 1000)
        return offset_play + (_deterministic_hash(raw_action) % 1000)

    return offset_other + 1
