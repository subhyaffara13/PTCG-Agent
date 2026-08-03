import random
from typing import Optional

def thompson_sample(cell: BanditCell, rng: Optional[random.Random] = None) -> float:
    """Draw a sample from Beta(alpha, beta). Returns a quality estimate in [0, 1]."""
    r = rng if rng is not None else random
    return r.betavariate(cell.alpha, cell.beta)

