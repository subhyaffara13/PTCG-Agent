
def log_graph_execution() -> None:
    """Emit a structured artifact with the graph execution order."""
    if not GRAPH_EXECUTION_ORDER:
        return
    try:
        trace_structured(
            "artifact",
            metadata_fn=lambda: {
                "name": "graph_execution",
                "encoding": "json",
            },
            payload_fn=lambda: {"graph_execution_order": GRAPH_EXECUTION_ORDER},
        )
    except Exception:
        log.debug("Failed to log graph_execution", exc_info=True)

