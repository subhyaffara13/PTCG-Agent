
def _hop_compile_and_call(fn, args, kwargs=None):
    """Compile and call fn with fullgraph=True for HOP eager execution.

    Pre-activates the fullgraph counter so that compile_wrapper treats this as
    a nested compile.  This avoids erroring when a non-infra dispatch mode
    causes the frame to be skipped — the function still executes eagerly within
    compile_wrapper and returns normally.
    """
    from torch._dynamo.eval_frame import set_fullgraph_compiled_frame_count

    with setup_compilation_env() as backend:
        old_count = set_fullgraph_compiled_frame_count(0)
        try:
            return torch.compile(fn, backend=backend, fullgraph=True)(
                *args, **(kwargs or {})
            )
        finally:
            set_fullgraph_compiled_frame_count(old_count)

