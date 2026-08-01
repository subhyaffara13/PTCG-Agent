
def _get_gc_statistics() -> Dict[str, Any]:
    """Get garbage collector statistics."""
    return {
        "enabled": gc.isenabled(),
        "thresholds": {
            "generation_0": gc.get_threshold()[0],
            "generation_1": gc.get_threshold()[1],
            "generation_2": gc.get_threshold()[2],
            "explanation": "Number of allocations before automatic collection for each generation",
        },
        "current_counts": {
            "generation_0": gc.get_count()[0],
            "generation_1": gc.get_count()[1],
            "generation_2": gc.get_count()[2],
            "explanation": "Current number of allocated objects in each generation",
        },
        "collection_history": [
            {
                "generation": i,
                "total_collections": stat["collections"],
                "total_collected": stat["collected"],
                "uncollectable": stat["uncollectable"],
            }
            for i, stat in enumerate(gc.get_stats())
        ],
    }

