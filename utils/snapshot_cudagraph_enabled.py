
def snapshot_cudagraph_enabled() -> bool:
    return torch._inductor.config.triton.cudagraphs

