
def vec_check_and_adjust_index(
    builder: LowLevelIRBuilder, lenv: Value, index: Value, line: int
) -> Value:
    r = Register(int64_rprimitive)
    index = builder.coerce(index, int64_rprimitive, line)
    lenv = builder.coerce(lenv, int64_rprimitive, line)
    ok, ok2, ok3 = BasicBlock(), BasicBlock(), BasicBlock()
    fail, fail2 = BasicBlock(), BasicBlock()
    is_less = builder.comparison_op(index, lenv, ComparisonOp.ULT, line)
    builder.add_bool_branch(is_less, ok2, fail)
    builder.activate_block(fail)

    x = builder.int_add(index, lenv)
    is_less2 = builder.comparison_op(x, lenv, ComparisonOp.ULT, line)
    builder.add_bool_branch(is_less2, ok, fail2)

    builder.activate_block(fail2)
    # TODO: Include index in exception
    builder.add(RaiseStandardError(RaiseStandardError.INDEX_ERROR, None, line))
    builder.add(Unreachable())

    builder.activate_block(ok)
    builder.assign(r, x)
    builder.goto(ok3)

    builder.activate_block(ok2)
    builder.assign(r, index)
    builder.goto(ok3)

    builder.activate_block(ok3)
    return r

