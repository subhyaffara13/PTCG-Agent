
def record_and_log_graph_execution_order() -> Iterator[None]:
    """Record graph execution order and log it once on exit."""
    global RECORD_GRAPH_EXECUTION, GRAPH_EXECUTION_ORDER, GRAPH_COMPILE_IDS
    GRAPH_EXECUTION_ORDER = []
    GRAPH_COMPILE_IDS = {}
    RECORD_GRAPH_EXECUTION = True
    try:
        yield
    finally:
        log_graph_execution()
        RECORD_GRAPH_EXECUTION = False
        GRAPH_EXECUTION_ORDER = None
        GRAPH_COMPILE_IDS = None

