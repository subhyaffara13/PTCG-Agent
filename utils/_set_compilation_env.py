
def _set_compilation_env():
    _old_is_tracing = torch.fx._symbolic_trace._is_fx_tracing_flag
    _old_allow_empty_graphs = torch._dynamo.config.allow_empty_graphs
    _old_capture_scalar_outputs = torch._dynamo.config.capture_scalar_outputs
    # The issue is tracked in https://github.com/pytorch/pytorch/issues/144360: when dynamo finds
    # the top-level frame produces no graph, the default behavior is to fallback to eager.
    # Then when it encounters an inner function, it will try to trace that function again, which is unnecessary.
    # For while_loop, during inspecting the inner call, we trace into the python dispathcer
    # logic, which is not tracable as of today. So the proper fix can be either 1. allow dispatch
    # logic to be dynamo tracable or 2. fixing https://github.com/pytorch/pytorch/issues/144360.
    # but it exposes some bugs in existing tests so we have to have a temporary flag to control
    # the behavior, which allows dynamo to store an empty graph for a frame without falling back to eager
    try:
        # We need to turn off the is_fx_tracing_flag. Remove this flag check from dyanmo
        # once we are confident fx tracing works with dynamo.
        torch.fx._symbolic_trace._is_fx_tracing_flag = False
        # pyrefly: ignore [bad-assignment]
        torch._dynamo.config.allow_empty_graphs = True
        torch._dynamo.config.capture_scalar_outputs = True
        yield
    finally:
        torch.fx._symbolic_trace._is_fx_tracing_flag = _old_is_tracing
        torch._dynamo.config.allow_empty_graphs = _old_allow_empty_graphs
        torch._dynamo.config.capture_scalar_outputs = _old_capture_scalar_outputs

