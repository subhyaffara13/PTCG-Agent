
def _count_initializer_size(graph: ir.Graph) -> int:
    """Count the total size of the initializers in bytes."""
    return sum(
        v.const_value.nbytes
        for v in graph.initializers.values()
        if v.const_value is not None
    )

