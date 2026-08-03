from typing import Optional, Tuple, Union

def _compute_mean_std_sem(data: np.ndarray, axis: Optional[int] = None) -> Tuple[Union[float, np.ndarray], Union[float, np.ndarray], Union[float, np.ndarray]]:
    """Unified logic for computing mean, StdDev and SEM, handling edge cases consistently.

    Optimized for speed by avoiding slow nanmean/nanstd and using masks directly.
    Supports both scalar inputs (axis=None) and vectorized inputs (axis=0 or 1 for bootstrapping).
    Returns (mean, stddev, sem).
    """
    mask = ~np.isnan(data)
    count = np.sum(mask, axis=axis)
    
    # Fill NaNs with 0 for summation
    clean_data = np.where(mask, data, 0.0)
    
    data_sum = np.sum(clean_data, axis=axis)
    mean = np.divide(data_sum, count, out=np.zeros_like(data_sum, dtype=np.float64), where=count > 0)
    
    # Variance: E[X^2] - (E[X])^2
    data_sq_sum = np.sum(clean_data**2, axis=axis)
    mean_sq = np.divide(data_sq_sum, count, out=np.zeros_like(data_sum, dtype=np.float64), where=count > 0)
    
    # Use max(0, var) to avoid tiny negative numbers due to precision
    var = np.maximum(0.0, mean_sq - mean**2)
    
    # Bessel's correction for sample variance: var * (n / (n-1))
    sample_var = np.divide(var * count, count - 1, out=np.zeros_like(var), where=count > 1)
    std = np.sqrt(sample_var)
    
    # SEM is std / sqrt(n)
    sem = np.divide(std, np.sqrt(count), out=np.zeros_like(std), where=count > 1)

    if axis is None:
        return float(mean), float(std), float(sem)
    return mean, std, sem

