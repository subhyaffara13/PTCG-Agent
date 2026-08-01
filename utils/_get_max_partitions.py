
def _get_max_partitions() -> int:
    """Get maximum partitions from config."""
    return getattr(config, "partitioned_scatter_max_partitions", 128)

