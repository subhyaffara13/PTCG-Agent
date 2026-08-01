
def remove_load_call_method(instructions: list[Instruction]) -> list[Instruction]:
    """LOAD_METHOD puts a NULL on the stack which causes issues, so remove it"""
    assert sys.version_info < (3, 11)
    rewrites = {"LOAD_METHOD": "LOAD_ATTR", "CALL_METHOD": "CALL_FUNCTION"}
    for inst in instructions:
        if inst.opname in rewrites:
            inst.opname = rewrites[inst.opname]
            inst.opcode = dis.opmap[inst.opname]
    return instructions

