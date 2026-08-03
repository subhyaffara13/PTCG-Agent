import time
from typing import Any

def get_fake_value(
    node: torch.fx.Node,
    tx: InstructionTranslatorBase,
    allow_non_graph_fake: bool = False,
) -> Any:
    _t0 = time.time_ns()
    try:
        return _get_fake_value_impl(node, tx, allow_non_graph_fake)
    finally:
        tx.output.bytecode_tracing_timings.get_fake_value_ns += time.time_ns() - _t0

