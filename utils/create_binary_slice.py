
def create_binary_slice(
    start: int | None, end: int | None, store: bool = False
) -> list[Instruction]:
    """
    BINARY_SLICE and STORE_SLICE (if `set` is True) for all Python versions
    """
    if sys.version_info >= (3, 14):
        subscr_inst = (
            create_instruction("STORE_SUBSCR") if store else create_binary_subscr()
        )
        return [
            create_load_const(slice(start, end)),
            subscr_inst,
        ]
    elif sys.version_info >= (3, 12):
        inst_name = "STORE_SLICE" if store else "BINARY_SLICE"
        return [
            create_load_const(start),
            create_load_const(end),
            create_instruction(inst_name),
        ]
    else:
        inst_name = "STORE_SUBSCR" if store else "BINARY_SUBSCR"
        return [
            create_load_const(start),
            create_load_const(end),
            create_instruction("BUILD_SLICE", arg=2),
            create_instruction(inst_name),
        ]

