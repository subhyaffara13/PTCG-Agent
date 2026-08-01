
def _temp_group_visit_leaves(snode: BaseSchedulerNode, fn):
    from torch._inductor.scheduler import GroupedSchedulerNode

    if isinstance(snode, GroupedSchedulerNode) and snode.temp_grouping:
        for _snode in snode.snodes:
            fn(_snode)
    else:
        fn(snode)

