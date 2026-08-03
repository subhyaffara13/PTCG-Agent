import sys

def create_copy(i: int) -> list[Instruction]:
    if sys.version_info >= (3, 11):
        return [create_instruction("COPY", arg=i)]
    if i == 1:
        return [create_instruction("DUP_TOP")]
    # COPY 4
    # 0 1 2 3
    # 3 1 2 0
    # 3 1 2 0 0
    # 0 1 2 0 3
    # 0 1 2 3 0
    return [
        *create_swap(i),
        create_dup_top(),
        *create_swap(i + 1),
        *create_swap(2),
    ]

