import random
from typing import List

def apply_symmetry_augmentation(state_tensor: List[float], stack_size: int, single_state_dim: int, max_hand: int, max_board: int) -> List[float]:
    """
    Data Augmentation: Shuffles the bench pokemon in the state tensor.
    """
    new_tensor = list(state_tensor)
    for frame in range(stack_size):
        offset = frame * single_state_dim
        bench_start = offset + max_hand + 1
        bench_end = bench_start + (max_board - 1)
        
        # Extract bench slice, shuffle non-zero elements
        bench_slice = new_tensor[bench_start:bench_end]
        active_elements = [x for x in bench_slice if x != 0.0]
        zeros = [0.0] * (len(bench_slice) - len(active_elements))
        
        random.shuffle(active_elements)
        new_bench = active_elements + zeros
        
        # Put back
        new_tensor[bench_start:bench_end] = new_bench
        
    return new_tensor

def normalize_action(raw_action: str, offset_play: int, offset_attack: int, offset_other: int) -> int:
    """Maps action string to integer action ID."""
    if not raw_action:
        return offset_other + 999  # Pass
        
    if raw_action.startswith("attack:"):
        return offset_attack + (hash(raw_action) % 1000)
        
    if raw_action.startswith("play:") or raw_action.startswith("play_") or raw_action.startswith("ability:") or raw_action.startswith("retreat:") or raw_action.startswith("attach_energy:") or raw_action.startswith("evolve:") or raw_action.startswith("bench:"):
        return offset_play + (hash(raw_action) % 1000)
            
    return offset_other + 1
