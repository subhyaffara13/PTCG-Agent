
def get_static_input_idxs(num_fixed: int) -> list[int]:
    # If we are inlining NNModules, we treat all torch.nn.Parameters as static for the purposes
    # of cudagraphs. Rather than copying these into cudagraph-owned memory
    # like we do for normal inputs on each run, we will re-record a cudagraph if these
    # parameter locations change.
    context = torch._guards.TracingContext.try_get()
    fixed = list(range(num_fixed))
    if not context or not context.fw_metadata:
        return fixed

    return context.fw_metadata.static_input_indices

