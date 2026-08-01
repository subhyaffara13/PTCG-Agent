
def get_allocated_khash_memory():
    snapshot = tracemalloc.take_snapshot()
    snapshot = snapshot.filter_traces(
        (tracemalloc.DomainFilter(True, ht.get_hashtable_trace_domain()),)
    )
    return sum(x.size for x in snapshot.traces)

