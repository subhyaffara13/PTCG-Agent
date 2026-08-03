from typing import Callable

def contains_collective(
    snode: BaseSchedulerNode,
    filter_fn: Callable[[BaseSchedulerNode], bool] | None = None,
) -> bool:
    from torch._inductor.scheduler import GroupedSchedulerNode

    if isinstance(snode, GroupedSchedulerNode):
        return any(contains_collective(x) for x in snode.snodes)

    return is_collective(snode.node) and (filter_fn is None or filter_fn(snode))

