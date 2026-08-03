from typing import Any

def populate_kw_names_argval(instructions: Sequence[Instruction], consts: Any) -> None:
    for inst in instructions:
        if inst.opname == "KW_NAMES":
            inst.argval = consts[inst.arg]

