
def unregister_cp_sharding_rules(clear_the_cache=False):
    """Unregister Context Parallelism sharding rules and restore original strategies."""
    global _cp_strategy_contexts, _original_strategies

    # Exit all context managers
    for ctx in _cp_strategy_contexts.values():
        ctx.__exit__(None, None, None)

    if clear_the_cache:
        _clear_fast_path_sharding_prop_cache()
        _clear_python_sharding_prop_cache()

    _cp_strategy_contexts = {}
    _original_strategies = {}

