from typing import Any, Callable

def _wrap_with_inductor_config(
    compiler_fn: Any, config_patches: dict[str, Any]
) -> Callable[..., Any]:
    """
    Wrap a compiler function to apply inductor config patches during compilation.

    Passes config_patches as a keyword argument so that compile_fx can
    propagate them to backward compilation via its inner_compile wrapping.
    """

    def wrapped(gm: Any, example_inputs: Any) -> Any:
        return compiler_fn(gm, example_inputs, config_patches=config_patches)

    # Preserve function metadata for logging
    wrapped.__name__ = getattr(compiler_fn, "__name__", "<wrapped>")
    wrapped.__wrapped__ = compiler_fn  # type: ignore[attr-defined]
    return wrapped

