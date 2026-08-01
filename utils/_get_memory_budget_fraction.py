
def _get_memory_budget_fraction() -> float:
    """Get memory budget fraction from config."""
    return getattr(config, "partitioned_scatter_memory_budget", 0.10)

