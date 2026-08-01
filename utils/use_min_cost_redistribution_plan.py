
def use_min_cost_redistribution_plan(enabled: bool = True):
    """
    Context manager to control the redistribution planning strategy for DTensor operations.

    This context manager allows you to choose between two algorithms for computing the
    sequence of collective operations needed to redistribute a DTensor from one placement
    to another:

    - **Graph-based**: Uses Dijkstra's algorithm to find the minimum-cost path
      through all possible placement transformations. This approach considers the global
      cost of all collective operations and finds the optimal sequence. Best for complex
      redistribution patterns where reducing communication cost and memory overhead is critical.

    - **Greedy**: Uses a heuristic approach that makes locally optimal choices
      at each step. This is faster to compute but may not produce the globally optimal
      transformation sequence. Best for simple redistribution patterns or when planning
      speed is more important than optimal communication.

    **Default Behavior (without this context manager):**

    When this context manager is NOT used, the algorithm selection follows this priority:

    1. **Non-default shard orders**
       → Always use graph-based algorithm (required for correctness)

    2. **Explicit `use_graph_based_transform` parameter** to `_gen_transform_infos_non_cached`
       → Use the specified algorithm (True = graph-based, False = greedy)

    3. **No explicit parameter** (default case)
       → Use greedy algorithm for faster planning

    **Behavior with this context manager:**

    This context manager overrides the default selection by setting the global flag
    `_FORCE_MIN_COST_REDISTRIBUTION_PLAN`, which takes precedence over the explicit
    `use_graph_based_transform` parameter (but not over non-default shard order requirements).

    **Cache Considerations:**

    The redistribution planner caches transform info for performance via the `@cache`
    decorator on `_gen_transform_infos`. If you need to change the algorithm selection
    for the same input specs, clear the cache using `_gen_transform_infos.cache_clear()`
    to ensure the new setting takes effect and doesn't reuse cached results from a
    previous run.

    Args:
        enabled (bool): If True, forces the use of the graph-based algorithm.
                       If False, forces the use of the greedy algorithm.
                       Default: True
    """
    global _FORCE_MIN_COST_REDISTRIBUTION_PLAN

    old_value = _FORCE_MIN_COST_REDISTRIBUTION_PLAN
    _FORCE_MIN_COST_REDISTRIBUTION_PLAN = enabled
    try:
        yield
    finally:
        _FORCE_MIN_COST_REDISTRIBUTION_PLAN = old_value

