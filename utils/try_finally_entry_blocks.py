
def try_finally_entry_blocks(
    builder: IRBuilder,
    err_handler: BasicBlock,
    return_entry: BasicBlock,
    main_entry: BasicBlock,
    finally_block: BasicBlock,
    ret_reg: Register | AssignmentTarget | None,
) -> Value:
    line = builder.fn_info.fitem.line
    old_exc = Register(exc_rtuple, line=line)

    # Entry block for non-exceptional flow
    builder.activate_block(main_entry)
    if ret_reg:
        builder.assign(ret_reg, builder.add(LoadErrorValue(builder.ret_types[-1], line)), line)
    builder.goto(return_entry)

    builder.activate_block(return_entry)
    builder.add(Assign(old_exc, builder.add(LoadErrorValue(exc_rtuple, line)), line))
    builder.goto(finally_block)

    # Entry block for errors
    builder.activate_block(err_handler)
    if ret_reg:
        builder.assign(ret_reg, builder.add(LoadErrorValue(builder.ret_types[-1], line)), line)
    builder.add(Assign(old_exc, builder.call_c(error_catch_op, [], line), line))
    builder.goto(finally_block)

    return old_exc

