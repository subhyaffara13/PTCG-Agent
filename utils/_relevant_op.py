
def _relevant_op(opcode: str | None) -> bool:
    """Check if opcode is relevant for variable assignment."""
    return bool(opcode and opcode.startswith("STORE_"))

