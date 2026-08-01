
def parse_memory_stats_unified(response, **kwargs):
    """Parse MEMORY STATS for unified RESP2 output.

    Unified responses decode structural keys while preserving string-like
    values as delivered, matching the approved RESP2/RESP3 unification shape.
    """
    stats = pairs_to_dict(response, decode_keys=True)
    for key, value in stats.items():
        if key.startswith("db.") and isinstance(value, list):
            stats[key] = pairs_to_dict(value, decode_keys=True)
    return stats

