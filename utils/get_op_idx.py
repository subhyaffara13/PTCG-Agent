
def get_op_idx(snode):
    assert not isinstance(
        snode,
        (
            torch._inductor.scheduler.FusedSchedulerNode,
            torch._inductor.scheduler.GroupedSchedulerNode,
        ),
    )
    return int(snode.get_name()[2:])

