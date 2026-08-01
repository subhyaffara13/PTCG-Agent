
def is_using_cudagraph_partition() -> bool:
    return (
        torch._inductor.config.triton.cudagraphs
        or _unstable_customized_partition_wrapper.wrapper is not None
    ) and torch._inductor.config.graph_partition

