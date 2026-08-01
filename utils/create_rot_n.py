
def create_rot_n(n: int) -> list[Instruction]:
    """
    Returns a "simple" sequence of instructions that rotates TOS to the n-th
    position in the stack. For Python < 3.11, returns a single ROT_*
    instruction. If no such instruction exists, an error is raised and the
    caller is expected to generate an equivalent sequence of instructions.
    For Python >= 3.11, any rotation can be expressed as a simple sequence of
    swaps.
    """
    if n <= 1:
        # don't rotate
        return []

    if sys.version_info >= (3, 11):
        # rotate can be expressed as a sequence of swap operations
        # e.g. rotate 3 is equivalent to swap 3, swap 2
        return [create_instruction("SWAP", arg=i) for i in range(n, 1, -1)]

    if n <= 4:
        return [create_instruction("ROT_" + ["TWO", "THREE", "FOUR"][n - 2])]
    return [create_instruction("ROT_N", arg=n)]

