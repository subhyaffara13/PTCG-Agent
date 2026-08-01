
def script_if_tracing(fn):
    """
    Compiles ``fn`` when it is first called during tracing.

    .. deprecated:: 2.5
        TorchScript is deprecated, please use ``torch.compile`` instead.

    ``torch.jit.script`` has a non-negligible start up time when it is first called due to
    lazy-initializations of many compiler builtins. Therefore you should not use
    it in library code. However, you may want to have parts of your library work
    in tracing even if they use control flow. In these cases, you should use
    ``@torch.jit.script_if_tracing`` to substitute for
    ``torch.jit.script``.

    Args:
        fn: A function to compile.

    Returns:
        If called during tracing, a :class:`ScriptFunction` created by `torch.jit.script` is returned.
        Otherwise, the original function `fn` is returned.
    """
    return _script_if_tracing(fn)

