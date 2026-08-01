
def _testing_capture_invoke_subgraph_inductor_compile_gms() -> Generator[
    list[torch.fx.GraphModule]
]:
    """
    Context manager to capture graph modules compiled by invoke_subgraph_inductor_compile.

    Usage:
        with _testing_capture_invoke_subgraph_inductor_compile_gms() as captured_gms:
            # code that triggers invoke_subgraph_inductor_compile
            pass
        # captured_gms will contain the list of captured graph modules
    """
    global _testing_invoke_subgraph_inductor_compile_captured_gms
    # pyrefly: ignore [implicit-any]
    _testing_invoke_subgraph_inductor_compile_captured_gms = []
    try:
        yield _testing_invoke_subgraph_inductor_compile_captured_gms
    finally:
        _testing_invoke_subgraph_inductor_compile_captured_gms = None

