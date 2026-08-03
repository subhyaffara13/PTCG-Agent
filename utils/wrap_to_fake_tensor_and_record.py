import time
from typing import Any

def wrap_to_fake_tensor_and_record(
    e: Any,
    tx: "InstructionTranslatorBase",
    *,
    source: Source | None,
    is_tensor: bool,
    parent_context: Any | None = None,
) -> Any:
    _t0 = time.time_ns()
    try:
        return _wrap_to_fake_tensor_and_record_impl(
            e, tx, source=source, is_tensor=is_tensor, parent_context=parent_context
        )
    finally:
        tx.output.bytecode_tracing_timings.wrap_to_fake_tensor_and_record_ns += (
            time.time_ns() - _t0
        )

