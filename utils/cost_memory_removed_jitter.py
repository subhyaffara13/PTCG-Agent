import random

def cost_memory_removed_jitter(size12: int, size1: int, size2: int, k12: int, k1: int, k2: int) -> float:
    """Like memory-removed, but with a slight amount of noise that breaks ties
    and thus jumbles the contractions a bit.
    """
    return random.gauss(1.0, 0.01) * (size12 - size1 - size2)

