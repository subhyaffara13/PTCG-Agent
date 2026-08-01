
def cleaned_instructions(code: types.CodeType, safe: bool = False) -> list[Instruction]:
    instructions = _cached_cleaned_instructions(code, safe)
    # We have a lot of code that implicitly mutates the instruction array. We
    # could do better here by making the copies explicit when necessary.
    return _clone_instructions(instructions)

