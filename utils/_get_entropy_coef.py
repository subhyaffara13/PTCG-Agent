
def _get_entropy_coef(entropy_start: float, entropy_end: float, progress: float) -> float:
    return entropy_start + (entropy_end - entropy_start) * progress

