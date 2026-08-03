from typing import Callable

def trace_structured_artifact(
    name: str,  # this will go in metadata
    encoding: str,
    payload_fn: Callable[[], str | object | None] = lambda: None,
    compile_id: CompileId | None = None,
) -> None:
    trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": name,
            "encoding": encoding,
        },
        payload_fn=payload_fn,
        compile_id=compile_id,
    )

