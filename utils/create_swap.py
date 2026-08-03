import sys

def create_swap(n: int) -> list[Instruction]:
    if sys.version_info >= (3, 11):
        return [create_instruction("SWAP", arg=n)]
    # in Python < 3.11, SWAP is a macro that expands to multiple instructions
    if n == 1:
        return []
    elif n == 2:
        return [create_instruction("ROT_TWO")]
    elif n == 3:
        return [create_instruction("ROT_THREE"), create_instruction("ROT_TWO")]
    """
    e.g. swap "a" and "b" in this stack:
    0 a 1 2 3 b
    0 a [1 2 3 b]
    0 a [1 2 3 b] [1 2 3 b]
    0 a [1 2 3 b] [1 2 3 b] -1
    0 a [1 2 3 b] b
    0 b a [1 2 3 b]
    0 b a [1 2 3 b] [1 2 3 b]
    0 b [1 2 3 b] a [1 2 3 b]
    0 b [1 2 3 b] a [1 2 3 b] -1
    0 b [1 2 3 a]
    0 b [1 2 3 a] [1 2 3 a]
    0 b [1 2 3 a] [1 2 3 a] reverse
    0 b [a 3 2 1] None
    0 b [a 3 2 1]
    0 b 1 2 3 a
    """
    return [
        create_instruction("BUILD_LIST", arg=n - 1),
        create_instruction("DUP_TOP"),
        create_instruction("LOAD_CONST", argval=-1),
        create_binary_subscr(),
        create_instruction("ROT_THREE"),
        create_instruction("DUP_TOP"),
        create_instruction("ROT_THREE"),
        create_instruction("LOAD_CONST", argval=-1),
        create_instruction("STORE_SUBSCR"),
        create_instruction("DUP_TOP"),
        create_load_method("reverse"),
        *create_call_method(0),
        create_instruction("POP_TOP"),
        create_instruction("UNPACK_SEQUENCE", arg=n - 1),
    ]

