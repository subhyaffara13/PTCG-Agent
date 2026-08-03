from typing import Any

def make_compile_context(compiled_autograd_id: int) -> Any:
    return compile_context(
        CompileContext(
            CompileId(
                compiled_autograd_id=compiled_autograd_id,
                frame_id=None,
                frame_compile_id=None,
            )
        )
    )

