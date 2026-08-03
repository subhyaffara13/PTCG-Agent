from typing import Any, Callable

def register_aoti_compile_backend(
    device_type: str,
    compile_fn: Callable[..., str],
    load_fn: Callable[[str, str, str], list[dict[str, Any] | None]],
) -> None:
    _aoti_compile_backends[device_type] = AOTICompileBackend(
        compile_fn=compile_fn,
        load_fn=load_fn,
    )

