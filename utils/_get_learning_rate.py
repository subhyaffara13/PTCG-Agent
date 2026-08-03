import math


def _get_learning_rate(lr_start: float, lr_end: float, progress: float) -> float:
    cosine_decay = 0.5 * (1.0 + math.cos(math.pi * progress))
    return lr_end + (lr_start - lr_end) * cosine_decay

