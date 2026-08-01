
def is_tracing(tensor=None) -> bool:
    """Checks whether we are tracing a graph with dynamo (compile or export), torch.jit, torch.fx, jax.jit (with torchax) or
    CUDA stream capturing or FakeTensor"""

    # Note that `is_torchdynamo_compiling` checks both compiling and exporting (the export check is stricter and
    # only checks export)
    _is_tracing = is_torchdynamo_compiling() or is_jit_tracing() or is_cuda_stream_capturing()
    if tensor is not None:
        _is_tracing |= is_torch_fx_proxy(tensor)
        _is_tracing |= is_fake_tensor(tensor)
        _is_tracing |= is_jax_jitting(tensor)

    return _is_tracing


def is_tracing():
    """Return a boolean value.

    Returns ``True`` in tracing (if a function is called during the
    tracing of code with ``torch.jit.trace``) and ``False`` otherwise.
    """
    if is_scripting():
        return False
    return torch._C._is_tracing()

