
def error_on_graph_break(
    error_on_graph_break: bool,
) -> ErrorOnGraphBreakDecoratorContextManager:
    """
    Context manager/decorator to toggle torch.compile's `error_on_graph_break` setting at compile time.

    If `fullgraph` is set, then `error_on_graph_break` does nothing
    (i.e. `fullgraph = True` takes higher precedence). If `fullgraph` is False, then
    `error_on_graph_break` determines whether `torch.compile` throws an error upon
    encountering a graph break, or attempts to continue tracing.

    `error_on_graph_break` can be toggled during compile time with this decorator to allow graph breaks in some
    compiled regions but not others. One key difference from `fullgraph` is that `error_on_graph_break = True`
    does NOT guarantee that a single graph is captured from the compiled function.

    The default value of torch.compile's `error_on_graph_break` setting is False.
    """
    return ErrorOnGraphBreakDecoratorContextManager(error_on_graph_break)

