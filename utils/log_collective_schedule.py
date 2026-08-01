
def log_collective_schedule(nodes: Sequence[BaseSchedulerNode]) -> None:
    schedule = [
        getattr(op, "python_kernel_name", None)
        for node in nodes
        if isinstance(op := getattr(node, "node", None), ir._CollectiveKernel)
    ]

    # Only log when there is at least one collective op
    if schedule:
        _dump_collective_schedule(schedule)

