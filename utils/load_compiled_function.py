from typing import Any, Callable

def load_compiled_function(
    file: io.IOBase,
    *,
    f_globals: dict[str, object] | None = None,
    external_data: dict[str, Any] | None = None,
) -> Callable[..., Any]:
    """
    Load an aot-compiled function from a file.

    .. warning::

        This API is currently experimental and subject to change.

    Args:
        file: A file-like object containing the serialized compiled function.
        f_globals: Optional global scope enclosing the compiled function.
        external_data: Optional data to be loaded into the runtime environment
                       of the compiled function. This should contains the same
                       data as AOTCompileResult.external_data returned from save_compiled_function() call.

    Returns:
        A torch-compiled function with compilation preloaded from disk.
    """
    from torch._dynamo.aot_compile import AOTCompiledFunction

    data = file.read()
    return AOTCompiledFunction.deserialize(data, f_globals, external_data)

