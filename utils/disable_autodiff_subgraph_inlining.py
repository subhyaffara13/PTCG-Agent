
def disable_autodiff_subgraph_inlining(enabled=True):
    torch._C._debug_set_autodiff_subgraph_inlining(not enabled)
    try:
        yield
    finally:
        torch._C._debug_set_autodiff_subgraph_inlining(True)

