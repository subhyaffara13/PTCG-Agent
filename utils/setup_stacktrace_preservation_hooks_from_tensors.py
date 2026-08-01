
def setup_stacktrace_preservation_hooks_from_tensors(outputs: Any) -> None:
    roots = [
        t.grad_fn
        for t in (outputs if isinstance(outputs, (list, tuple)) else (outputs,))
        if isinstance(t, torch.Tensor) and t.grad_fn is not None
    ]
    if roots:
        setup_stacktrace_preservation_hooks(roots)

