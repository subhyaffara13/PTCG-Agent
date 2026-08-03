import functools

def aggregate_origins(
    node_schedule: Sequence[BaseSchedulerNode] | ExternKernel,
) -> OrderedSet[Node]:
    from . import ir

    if isinstance(node_schedule, list):
        return functools.reduce(
            operator.or_,
            [
                # pyrefly: ignore [missing-attribute]
                node.node.origins
                for node in node_schedule
                if hasattr(node, "node") and node.node
            ],
            OrderedSet(),
        )
    elif isinstance(node_schedule, ir.ExternKernel):
        return node_schedule.origins
    else:
        return OrderedSet()

