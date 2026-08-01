
def _walk_global_ops(code):
    """Yield referenced name for global-referencing instructions in code."""
    for instr in dis.get_instructions(code):
        op = instr.opcode
        if op in GLOBAL_OPS:
            yield instr.argval

