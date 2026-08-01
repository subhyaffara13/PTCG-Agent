
def sink_waits_iterative(snodes: list[BaseSchedulerNode]) -> list[BaseSchedulerNode]:
    """
    Similarly to reorder_communication_preserving_peak_memory this pass will try to iteratively
    push Wait nodes later, recomputing estimated peak memory before each swap,
    and preventing peak memory regressions.

    Pass will be applied to every Wait node. If there are immediate dependencies with next node,
    pass will try to group them together and on the next step to swap the group with next candidate.

    If _inductor.config_comms.sink_iterative_use_runtime_estimations is set True,
    pass will stop reordering of Wait once corresponding Collective is unexposed,
    based on runtime estimations.

    inductor.config_comms.sink_iterative_peak_memory_budget allows to tune how much pass
    can regress initial peak memory.
    E.g.:
    sink_iterative_peak_memory_budget == 0.0 - No regression of initial peak memory is allowed
    sink_iterative_peak_memory_budget == 0.2 - Pass can improve comm-compute overlap, sacrificing
    20% of initial peak memory value.

    inductor.config_comms.sink_iterative_extra_comm_comp_overlap config allows to more aggressively
    sink waits, stopping only when overlap_compute >= (1 + extra_comm_comp_overlap) * comm_time
    """
    return _sink_waits_iterative_internal(snodes)[0]

