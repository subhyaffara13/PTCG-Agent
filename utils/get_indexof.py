
def get_indexof(insts: list["Instruction"]) -> dict["Instruction", int]:
    """
    Get a mapping from instruction memory address to index in instruction list.
    Additionally checks that each instruction only appears once in the list.
    """
    # pyrefly: ignore [implicit-any]
    indexof = {}
    for i, inst in enumerate(insts):
        assert inst not in indexof
        indexof[inst] = i
    return indexof

