import sys

def create_call_method(nargs: int) -> list[Instruction]:
    if sys.version_info >= (3, 12):
        return [create_instruction("CALL", arg=nargs)]
    if sys.version_info >= (3, 11):
        return [
            create_instruction("PRECALL", arg=nargs),
            create_instruction("CALL", arg=nargs),
        ]
    return [create_instruction("CALL_METHOD", arg=nargs)]

