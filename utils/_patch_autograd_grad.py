
def _patch_autograd_grad():
    """Patch autograd.grad for non-strict make_fx tracing.

    This patch installs autograd hooks so traced backward nodes preserve
    stack trace, seq_nr, and autograd_backward metadata before delegating to
    the real torch.autograd.grad.
    """
    import functools

    import torch.autograd
    from torch._functorch._aot_autograd.logging_utils import (
        setup_stacktrace_preservation_hooks_from_tensors,
    )

    _orig_grad = torch.autograd.grad

    @functools.wraps(_orig_grad)
    def _patched_grad(outputs, inputs, *args, **kwargs):
        if not _is_non_strict_tracing():
            raise AssertionError(
                "_patch_autograd_grad() must be used under "
                "_non_strict_tracing_context()"
            )

        setup_stacktrace_preservation_hooks_from_tensors(outputs)
        return _orig_grad(outputs, inputs, *args, **kwargs)

    torch.autograd.grad = _patched_grad
    try:
        yield
    finally:
        torch.autograd.grad = _orig_grad

