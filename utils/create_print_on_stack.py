import sys

def create_print_on_stack(depth: int) -> list[Instruction]:
    return [
        *add_push_null(create_instruction("LOAD_CONST", argval=print)),
        *create_copy(depth + (2 if sys.version_info >= (3, 11) else 1)),
        *create_call_function(1, False),
        create_instruction("POP_TOP"),
    ]

