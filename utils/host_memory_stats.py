from typing import Any

def host_memory_stats() -> dict[str, Any]:
    r"""Return a dictionary of pinned (host) allocator statistics.

    Core statistics (host pinned allocator):

    - ``"allocations.{current,peak,allocated,freed}"``:
      pinned blocks owned by the allocator (active + cached). Grows when a new
      block is created via CUDA and shrinks when cached blocks are returned.
    - ``"allocated_bytes.{current,peak,allocated,freed}"``:
      bytes of pinned blocks owned by the allocator (active + cached), using
      the rounded block size requested from CUDA.
    - ``"active_requests.{current,peak,allocated,freed}"``:
      blocks currently checked out to callers (increments on handout, decrements
      when the block becomes reusable after stream deps finish).
    - ``"active_bytes.{current,peak,allocated,freed}"``:
      bytes corresponding to active blocks.

    Metric type:

    - ``current``: current value.
    - ``peak``: maximum value.
    - ``allocated``: historical total increase.
    - ``freed``: historical total decrease.

    Event/timing counters:

    - ``"num_host_alloc"`` / ``"num_host_free"``: blocks created to grow the
      pool / cached blocks returned to CUDA (matches allocations allocated/freed).
    - ``"host_alloc_time.{total,max,min,count,avg}"``: time in CUDA alloc calls
      when growing the pool (microseconds).
    - ``"host_free_time.{total,max,min,count,avg}"``: time in CUDA free calls
      when cached blocks are returned (microseconds).

    Block sizes are rounded up to the next power of two before calling CUDA, so
    byte stats reflect the rounded size. Peak values are aggregated per bucket
    and are a best-effort approximation of the true peak.
    """
    result = []

    def _recurse_add_to_result(prefix, obj):
        if isinstance(obj, dict):
            if len(prefix) > 0:
                prefix += "."
            for k, v in obj.items():
                _recurse_add_to_result(prefix + k, v)
        else:
            result.append((prefix, obj))

    stats = host_memory_stats_as_nested_dict()
    _recurse_add_to_result("", stats)
    result.sort()

    return collections.OrderedDict(result)

