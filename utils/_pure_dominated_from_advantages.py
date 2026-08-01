
def _pure_dominated_from_advantages(advantages, mode, tol=1e-7):
  if mode == DominanceType.DOMINANCE_STRICT:
    return (advantages > tol).all(1)
  if mode == DominanceType.DOMINANCE_WEAK:
    return (advantages >= -tol).all(1) & (advantages.sum(1) > tol)
  if mode == DominanceType.DOMINANCE_VERY_WEAK:
    return (advantages >= -tol).all(1)

