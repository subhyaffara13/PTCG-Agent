
def create_instruction(
    name: str,
    *,
    arg: int | None = None,
    argval: Any | None = _NotProvided,
    target: Instruction | None = None,
) -> Instruction:
    """
    At most one of `arg`, `argval`, and `target` can be not None/_NotProvided.
    This is to prevent ambiguity, e.g. does
        create_instruction("LOAD_CONST", 5)
    mean load the constant at co_consts[5], or load the constant 5?

    If `arg` is not provided, it will be computed during assembly from
    `argval` or `target`.

    Bits in the args of instructions LOAD_GLOBAL, LOAD_ATTR (3.12+), and LOAD_SUPER_ATTR
    modify the behavior of the instruction. In this case, we allow both `arg`
    and `argval` to be set. The value of `arg` here is expected to be the value of
    the op bits and the true value of `arg` will be computed during assembly.
    If `arg` is not set, the bits are assumed to be 0.
    """

    # allow for instructions with op bits to have both arg and argval specified
    if inst_has_op_bits(name):
        if target is not None:
            raise RuntimeError("target cannot be specified for instruction")
        if arg is None:
            arg = 0
    else:
        cnt = (arg is not None) + (argval is not _NotProvided) + (target is not None)
        if cnt > 1:
            raise RuntimeError(
                "only one of arg, argval, and target can be not None/_NotProvided"
            )
    if arg is not None and not isinstance(arg, int):
        raise RuntimeError("instruction arg must be int or None")
    return Instruction(
        opcode=dis.opmap[name], opname=name, arg=arg, argval=argval, target=target
    )

