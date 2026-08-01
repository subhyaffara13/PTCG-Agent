
def parse_memory_stats_resp3(response, **kwargs):
    """Parse the results of MEMORY STATS on RESP3 wire.

    Each entry arrives as a top-level ``dict`` instead of a flat list of
    pairs; decode the keys to ``str`` and recurse into the per-database
    ``db.*`` sub-dicts so the Python shape matches what
    :func:`parse_memory_stats` produces from RESP2 wire.
    """
    stats = {str_if_bytes(key): value for key, value in response.items()}
    for key, value in stats.items():
        if key.startswith("db.") and isinstance(value, dict):
            stats[key] = {str_if_bytes(k): v for k, v in value.items()}
    return stats

