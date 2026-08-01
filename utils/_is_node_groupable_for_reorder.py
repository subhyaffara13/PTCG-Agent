
def _is_node_groupable_for_reorder(
    candidate: BaseSchedulerNode,
) -> tuple[bool, str | None]:
    """
    Check if a candidate node can be grouped with collective during reordering.

    This pass processes collectives left to right, so we avoid grouping with
    already-processed collectives based on configuration.

    Args:
        candidate: Node to check for groupability

    Returns:
        Tuple of (is_groupable, reason_if_not_groupable)
    """
    # This pass processes collectives left to right,
    # Do not group with processed collectives.
    # Leaving config for experimentation in 2D
    if not config_comms.reorder_iterative_group_with_collectives:
        if contains_async_collective(candidate):
            return (
                False,
                f"candidate contains_collective {candidate.get_name()}",
            )
    if not config_comms.reorder_iterative_use_runtime_estimations:
        if contains_gemm_like(candidate):
            return False, "contains_gemm_like"
    return True, None

