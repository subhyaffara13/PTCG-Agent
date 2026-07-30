from . import dataclass

class BufferStats:
    expert_count: int
    self_play_count: int
    sample_count: int
    expert_actual_ratio: float

