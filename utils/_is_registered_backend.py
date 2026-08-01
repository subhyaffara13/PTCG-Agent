
def _is_registered_backend(compiler_fn: CompilerFn) -> bool:
    """
    Check if the given compiler function is a registered backend.
    Custom backends (user-provided callables not in the registry) return False.
    """
    # Ensure backends are loaded
    _lazy_import()

    # Check if it's directly a registered backend function
    if compiler_fn in _COMPILER_FNS.values():
        return True

    # Check for _TorchCompileInductorWrapper or _TorchCompileWrapper
    # These have a compiler_name attribute that identifies the backend
    if hasattr(compiler_fn, "compiler_name"):
        compiler_name = compiler_fn.compiler_name
        if compiler_name in _BACKENDS or compiler_name in _COMPILER_FNS:
            return True

    # Check if the wrapper has a compiler_fn attribute (e.g., _TorchCompileWrapper)
    if hasattr(compiler_fn, "compiler_fn"):
        return compiler_fn.compiler_fn in _COMPILER_FNS.values()

    return False

