
def append_numbers_notes(
    notes: list[str], arg_type: Instance, expected_type: Instance
) -> list[str]:
    """Explain if an unsupported type from "numbers" is used in a subtype check."""
    if expected_type.type.fullname in UNSUPPORTED_NUMBERS_TYPES:
        notes.append('Types from "numbers" are not supported for static type checking')
        notes.append("See https://peps.python.org/pep-0484/#the-numeric-tower")
        notes.append("Consider using a protocol instead, such as typing.SupportsFloat")
    return notes

