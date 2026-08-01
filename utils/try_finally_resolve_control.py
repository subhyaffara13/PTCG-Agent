
def try_finally_resolve_control(
    builder: IRBuilder,
    cleanup_block: BasicBlock,
    finally_control: FinallyNonlocalControl,
    old_exc: Value,
    ret_reg: Register | AssignmentTarget | None,
) -> BasicBlock:
    """Resolve the control flow out of a finally block.

    This means returning if there was a return, propagating
    exceptions, break/continue (soon), or just continuing on.
    """
    line = builder.fn_info.fitem.line
    reraise, rest = BasicBlock(), BasicBlock()
    builder.add(Branch(old_exc, rest, reraise, Branch.IS_ERROR, line))

    # Reraise the exception if there was one
    builder.activate_block(reraise)
    builder.call_c(reraise_exception_op, [], NO_TRACEBACK_LINE_NO)
    builder.add(Unreachable(line))
    builder.builder.pop_error_handler()

    # If there was a return, keep returning
    if ret_reg:
        builder.activate_block(rest)
        return_block, rest = BasicBlock(), BasicBlock()
        # For spill targets in try/finally, use nullable read to avoid AttributeError
        if isinstance(ret_reg, AssignmentTargetAttr) and ret_reg.attr.startswith(TEMP_ATTR_NAME):
            ret_val = builder.read_nullable_attr(ret_reg.obj, ret_reg.attr, line)
        else:
            ret_val = builder.read(ret_reg, line)
        builder.add(Branch(ret_val, rest, return_block, Branch.IS_ERROR, line))

        builder.activate_block(return_block)
        builder.nonlocal_control[-1].gen_return(builder, ret_val, line)

    # TODO: handle break/continue
    builder.activate_block(rest)
    out_block = BasicBlock()
    builder.goto(out_block)

    # If there was an exception, restore again
    builder.activate_block(cleanup_block)
    finally_control.gen_cleanup(builder, line)
    builder.call_c(keep_propagating_op, [], NO_TRACEBACK_LINE_NO)
    builder.add(Unreachable())

    return out_block

