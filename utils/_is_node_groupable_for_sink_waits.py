
def _is_node_groupable_for_sink_waits(
    candidate: BaseSchedulerNode,
) -> tuple[bool, str | None]:
    """
    Check if a candidate node can be grouped during sink_waits pass.

    Sink Waits traverses waits right to left, so we don't group with
    processed waits on the right or with async collectives.

    Args:
        candidate: Node to check for groupability

    Returns:
        Tuple of (is_groupable, reason_if_not_groupable)
    """
    # Sink Waits traverse Waits right to left,
    # => we do not group with processed Waits on the right.
    if contains_wait(candidate):
        return False, f"candidate contains wait {candidate.get_name()}"
    if contains_async_collective(candidate):
        return (
            False,
            f"candidate contains_async_collective {candidate.get_name()}",
        )

    if not config_comms.sink_iterative_use_runtime_estimations:
        # Heuristics pre-use_runtime_estimations:
        # TODO(ivankobzarev): Remove them after confirming,
        # that using runtime estimations always give better results.
        # We do not want to group with collectives to not reorder them forward.
        if contains_collective(candidate):
            return (
                False,
                f"candidate contains collective {candidate.get_name()}",
            )
        if contains_gemm_like(candidate):
            return (
                False,
                f"candidate contains gemm_like {candidate.get_name()}",
            )
    return True, None

