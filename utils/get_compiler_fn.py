from typing import Any, Callable

def get_compiler_fn(
    compiler_fn: str | Callable[..., Any] | None,
) -> WrapBackendDebug:
    from .repro.after_dynamo import wrap_backend_debug

    if compiler_fn is None:
        # Special case None to avoid crashing in hasattr
        compiler_str = None
    elif hasattr(compiler_fn, "compiler_name"):
        compiler_str = compiler_fn.compiler_name  # type: ignore[union-attr]
        assert isinstance(compiler_str, str)
    elif isinstance(compiler_fn, str):
        compiler_str = compiler_fn
    else:
        compiler_str = None
    compiler_fn = lookup_backend(compiler_fn)  # type: ignore[arg-type]
    return wrap_backend_debug(compiler_fn, compiler_str)

