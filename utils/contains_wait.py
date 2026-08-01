
def contains_wait(snode: BaseSchedulerNode) -> bool:
    from torch._inductor.scheduler import GroupedSchedulerNode

    if isinstance(snode, GroupedSchedulerNode):
        return any(contains_wait(x) for x in snode.snodes)
    else:
        return is_wait(snode.node)

