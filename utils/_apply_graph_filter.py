from typing import Callable

def _apply_graph_filter(
    filter_fn: Callable[[str, str, _OverrideNode], bool],
    *,
    reregister_overrides: bool = False,
) -> None:
    """
    Apply a filter function to remove nodes from graphs.

    This is a convenience function that uses the graph transformation pattern
    to filter out unwanted nodes.

    Args:
        filter_fn: Function that takes (op_symbol, dispatch_key, node) and
            returns True to keep the node, False to remove it
        reregister_overrides: Whether to reregister modified graphs

    Example:
        # Remove all nodes with "deprecated" in the DSL name
        _apply_graph_filter(
            lambda op, dk, node: "deprecated" not in node.dsl_name,
            reregister_overrides=True
        )

    Note:
        If filter_fn raises an exception for a specific graph, the original
        graph will be preserved and processing will continue.
    """

    def filtering_transformation(
        op_symbol: str, dispatch_key: str, graph: list[_OverrideNode]
    ) -> list[_OverrideNode]:
        """Apply filter_fn to graph with error handling."""
        try:
            return [node for node in graph if filter_fn(op_symbol, dispatch_key, node)]
        except (TypeError, ValueError, AttributeError, RuntimeError):
            log.warning(
                "Graph transformation failed for %s/%s. Preserving original graph.",
                op_symbol,
                dispatch_key,
                exc_info=True,
            )
            return graph
        except Exception:
            log.exception(
                "Unexpected error in graph transformation for %s/%s. Preserving original graph.",
                op_symbol,
                dispatch_key,
            )
            return graph

    _apply_graph_transformation(
        transformation_fn=filtering_transformation,
        reregister_overrides=reregister_overrides,
    )

