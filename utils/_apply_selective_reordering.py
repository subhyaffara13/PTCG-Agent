from typing import Callable

def _apply_selective_reordering(
    condition_fn: Callable[[str, str], bool],
    ordering_fn: UserOrderingFn,
    *,
    reregister_overrides: bool = False,
) -> None:
    """
    Apply reordering only to graphs that match a condition.

    This allows for more targeted reordering operations.

    Args:
        condition_fn: Function that takes (op_symbol, dispatch_key) and
            returns True if the graph should be reordered
        ordering_fn: Ordering function to apply to matching graphs
        reregister_overrides: Whether to reregister modified graphs

    Example:
        # Only reorder CUDA operations
        _apply_selective_reordering(
            condition_fn=lambda op, dk: dk == "CUDA",
            ordering_fn=lambda op, dk, g: sorted(g, key=lambda n: n.dsl_name),
            reregister_overrides=True
        )

    Note:
        If condition_fn or ordering_fn raises an exception for a specific graph,
        the original graph will be preserved and processing will continue.
    """

    def conditional_transformation(
        op_symbol: str, dispatch_key: str, graph: list[_OverrideNode]
    ) -> list[_OverrideNode]:
        """Apply ordering_fn conditionally based on condition_fn result."""
        try:
            should_reorder = condition_fn(op_symbol, dispatch_key)
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

        if should_reorder:
            try:
                return ordering_fn(op_symbol, dispatch_key, graph)
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

        return graph  # Return unchanged if condition doesn't match

    _apply_graph_transformation(
        transformation_fn=conditional_transformation,
        reregister_overrides=reregister_overrides,
    )

