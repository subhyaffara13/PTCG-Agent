from typing import Tuple

def calculate_sample_sizes(batch_size: int, expert_ratio: float, expert_len: int, self_play_len: int) -> Tuple[int, int]:
    target_expert = int(batch_size * expert_ratio)
    target_self_play = batch_size - target_expert
    
    actual_expert = min(target_expert, expert_len)
    if actual_expert < target_expert:
        target_self_play += (target_expert - actual_expert)
        
    actual_self_play = min(target_self_play, self_play_len)
    if actual_self_play < target_self_play:
        needed = target_self_play - actual_self_play
        extra_expert = min(needed, expert_len - actual_expert)
        actual_expert += extra_expert
        
    return actual_expert, actual_self_play

