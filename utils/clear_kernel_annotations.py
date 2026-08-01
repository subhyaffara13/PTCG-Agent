
def clear_kernel_annotations() -> None:
    """Clear all recorded kernel annotations and pending scopes."""
    global _capture_graph
    _kernel_annotations.clear()
    _pending_scopes.clear()
    _capture_graph = None

