from typing import List, Tuple

def _mean_sem(values: List[float]) -> Tuple[float, float]:
    """Helper to calculate mean and standard error of the mean.

    Args:
        values: A list of numerical values.

    Returns:
        A tuple (mean, sem). Returns (0.0, 0.0) if the list is empty.
    """
    if not values:
        return 0.0, 0.0
    mean, std, sem = _compute_mean_std_sem(np.asarray(values))
    return mean, sem

