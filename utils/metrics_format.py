
def metrics_format(metrics: dict[str, float]) -> dict[str, float]:
    """
    Reformat Trainer metrics values to a human-readable format.

    Args:
        metrics (`dict[str, float]`):
            The metrics returned from train/evaluate/predict

    Returns:
        metrics (`dict[str, float]`): The reformatted metrics
    """

    metrics_copy = metrics.copy()
    for k, v in metrics_copy.items():
        if "_mem_" in k:
            metrics_copy[k] = f"{v >> 20}MB"
        elif "_runtime" in k:
            metrics_copy[k] = _secs2timedelta(v)
        elif k == "total_flos":
            metrics_copy[k] = f"{int(v) >> 30}GF"
        elif isinstance(metrics_copy[k], float):
            metrics_copy[k] = round(v, 4)

    return metrics_copy

