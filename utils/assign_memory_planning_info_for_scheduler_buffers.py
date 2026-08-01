
def assign_memory_planning_info_for_scheduler_buffers(
    nodes: list[BaseSchedulerNode],
    name_to_buf: dict[str, SchedulerBuffer],
) -> None:
    """
    For each SchedulerBuffer, assign its size info and successor nodes.
    A buffer's successor nodes determines when a buffer can be freed.
    """
    # get buffer sizes
    sched_buf_to_size = compute_size_for_scheduler_buffer(name_to_buf)

    # get buffer's successor nodes for memory lifetime (excludes is_fake WeakDeps)
    # and for ordering (includes all deps)
    dep_name_to_succ_nodes: dict[str, OrderedSet[BaseSchedulerNode]] = (
        collections.defaultdict(OrderedSet)
    )
    dep_name_to_succ_nodes_for_ordering: dict[str, OrderedSet[BaseSchedulerNode]] = (
        collections.defaultdict(OrderedSet)
    )
    for node in nodes:
        for dep in node.unmet_dependencies:
            # All deps contribute to ordering, but fake weak deps do not contribute to
            # memory liveness
            dep_name_to_succ_nodes_for_ordering[dep.name].add(node)
            if not (isinstance(dep, WeakDep) and dep.is_fake):
                dep_name_to_succ_nodes[dep.name].add(node)

    # iterate in reverse, so dependencies are picked up transitively.
    for mutating_buf_name, real_buf_name in reversed(
        V.graph.scheduler.mutation_real_name.items()
    ):
        dep_name_to_succ_nodes[real_buf_name] |= dep_name_to_succ_nodes[
            mutating_buf_name
        ]
        dep_name_to_succ_nodes_for_ordering[real_buf_name] |= (
            dep_name_to_succ_nodes_for_ordering[mutating_buf_name]
        )

    # populate the MemoryPlanningInfoForBuffer attribute to each scheduler buffer
    # note: there are scheduler buffers not in dep_name_to_succ_nodes (e.g., graph outputs)
    for buf_name in name_to_buf:
        name_to_buf[buf_name].mpi_buffer = MemoryPlanningInfoForBuffer(
            size_alloc=sched_buf_to_size[buf_name][0],
            size_free=sched_buf_to_size[buf_name][1],
            succ_nodes=dep_name_to_succ_nodes[buf_name],
            succ_nodes_for_ordering=dep_name_to_succ_nodes_for_ordering[buf_name],
        )

