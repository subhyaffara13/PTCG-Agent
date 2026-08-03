from typing import Any, Callable

def post_compile(
    wrappers: list[CompilerWrapper],
    compiled_fn: Callable[..., Any],
    aot_config: AOTConfig,
    *,
    runtime_metadata: ViewAndMutationMeta,
) -> tuple[Callable[..., Any], ViewAndMutationMeta]:
    """
    Runs a sequence of wrappers on the given function. Should be called after pre_compile()
    """
    for wrapper in reversed(wrappers):
        compiled_fn = wrapper.post_compile(
            compiled_fn, aot_config, runtime_metadata=runtime_metadata
        )
    return compiled_fn, runtime_metadata

