from typing import Any

def ensure_graph_fake(e: Any, tx: InstructionTranslatorBase) -> Any:
    assert maybe_get_fake_mode(e) is tx.fake_mode
    return e

