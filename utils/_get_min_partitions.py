
def _get_min_partitions() -> int:
    """Get minimum partitions from config."""
    return getattr(config, "partitioned_scatter_min_partitions", 2)

