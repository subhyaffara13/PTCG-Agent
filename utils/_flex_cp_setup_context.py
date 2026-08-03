from typing import Any

def _flex_cp_setup_context(ctx: Any, inputs: Any, output: Any) -> None:
    _, _, ctx.seq_dim, ctx.pg_name = inputs

