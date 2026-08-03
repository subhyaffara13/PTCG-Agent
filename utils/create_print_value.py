from typing import Any

def create_print_value(value: Any) -> list[Instruction]:
    return [
        *add_push_null(create_instruction("LOAD_CONST", argval=print)),
        create_instruction("LOAD_CONST", argval=value),
        *create_call_function(1, False),
        create_instruction("POP_TOP"),
    ]

