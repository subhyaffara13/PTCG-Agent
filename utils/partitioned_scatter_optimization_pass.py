
def partitioned_scatter_optimization_pass(graph: fx.Graph) -> fx.Graph:
    """
    Apply partitioned scatter optimization to high-contention index_put operations.

    Reduces atomic contention by distributing writes across multiple buffers.
    Controlled by: config.partitioned_scatter_enabled
    """
    if not getattr(config, "partitioned_scatter_enabled", False):
        return graph

    num_matches = partitioned_scatter_patterns.apply(graph)

    if num_matches > 0:
        log.info(
            "partitioned_scatter_optimization: applied to %d operation(s)",
            num_matches,
        )
        graph.lint()

    return graph

