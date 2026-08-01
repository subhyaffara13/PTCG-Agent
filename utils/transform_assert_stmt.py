
def transform_assert_stmt(builder: IRBuilder, a: AssertStmt) -> None:
    if builder.options.strip_asserts:
        return
    cond = builder.accept(a.expr)
    ok_block, error_block = BasicBlock(), BasicBlock()
    builder.add_bool_branch(cond, ok_block, error_block)
    builder.activate_block(error_block)
    if a.msg is None:
        # Special case (for simpler generated code)
        builder.add(RaiseStandardError(RaiseStandardError.ASSERTION_ERROR, None, a.line))
    elif isinstance(a.msg, StrExpr):
        # Another special case
        builder.add(RaiseStandardError(RaiseStandardError.ASSERTION_ERROR, a.msg.value, a.line))
    else:
        # The general case -- explicitly construct an exception instance
        message = builder.accept(a.msg)
        exc_type = builder.load_module_attr_by_fullname("builtins.AssertionError", a.line)
        exc = builder.py_call(exc_type, [message], a.line)
        builder.call_c(raise_exception_op, [exc], a.line)
    builder.add(Unreachable())
    builder.activate_block(ok_block)

