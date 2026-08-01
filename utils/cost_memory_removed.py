
def cost_memory_removed(size12: int, size1: int, size2: int, k12: int, k1: int, k2: int) -> float:
    """The default heuristic cost, corresponding to the total reduction in
    memory of performing a contraction.
    """
    return size12 - size1 - size2

