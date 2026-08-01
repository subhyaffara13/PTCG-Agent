
def get_assert_bytecode_sequence(with_msg: bool) -> list[str]:
    if with_msg:

        def fn(x: Any) -> None:
            assert x, "msg"
    else:

        def fn(x: Any) -> None:
            assert x

    insts = [inst.opname for inst in dis.get_instructions(fn)]

    # expect to find POP_JUMP_[FORWARD_]IF_TRUE
    begin_idx = next(i for i, inst in enumerate(insts) if inst.startswith("POP_JUMP"))
    end_idx = insts.index("RAISE_VARARGS")

    return insts[begin_idx + 1 : end_idx + 1]

