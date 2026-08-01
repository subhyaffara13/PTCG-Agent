
def contains_gemm_like(snode: BaseSchedulerNode) -> bool:
    from torch._inductor.scheduler import GroupedSchedulerNode

    if isinstance(snode, GroupedSchedulerNode):
        return any(contains_gemm_like(x) for x in snode.snodes)
    else:
        return is_gemm_like(snode.node)

