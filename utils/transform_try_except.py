
def transform_try_except(
    builder: IRBuilder,
    body: GenFunc,
    handlers: Sequence[tuple[tuple[ValueGenFunc, int] | None, Expression | None, GenFunc]],
    else_body: GenFunc | None,
    line: int,
) -> None:
    """Generalized try/except/else handling that takes functions to gen the bodies.

    The point of this is to also be able to support with."""
    assert handlers, "try needs except"

    except_entry, exit_block, cleanup_block = BasicBlock(), BasicBlock(), BasicBlock()
    double_except_block = BasicBlock()
    # If there is an else block, jump there after the try, otherwise just leave
    else_block = BasicBlock() if else_body else exit_block

    # Compile the try block with an error handler
    builder.builder.push_error_handler(except_entry)
    builder.goto_and_activate(BasicBlock())
    body()
    builder.goto(else_block)
    builder.builder.pop_error_handler()

    # The error handler catches the error and then checks it
    # against the except clauses. We compile the error handler
    # itself with an error handler so that it can properly restore
    # the *old* exc_info if an exception occurs.
    # The exception chaining will be done automatically when the
    # exception is raised, based on the exception in exc_info.
    builder.builder.push_error_handler(double_except_block)
    builder.activate_block(except_entry)
    old_exc = builder.maybe_spill(builder.call_c(error_catch_op, [], line))
    # Compile the except blocks with the nonlocal control flow overridden to clear exc_info
    builder.nonlocal_control.append(ExceptNonlocalControl(builder.nonlocal_control[-1], old_exc))

    # Process the bodies
    for type, var, handler_body in handlers:
        next_block = None
        if type:
            type_f, type_line = type
            next_block, body_block = BasicBlock(), BasicBlock()
            matches = builder.call_c(exc_matches_op, [type_f()], type_line)
            builder.add(Branch(matches, body_block, next_block, Branch.BOOL, type_line))
            builder.activate_block(body_block)
        if var:
            target = builder.get_assignment_target(var)
            builder.assign(target, builder.call_c(get_exc_value_op, [], var.line), var.line)
        handler_body()
        builder.goto(cleanup_block)
        if next_block:
            builder.activate_block(next_block)

    # Reraise the exception if needed
    if next_block:
        builder.call_c(reraise_exception_op, [], NO_TRACEBACK_LINE_NO)
        builder.add(Unreachable())

    builder.nonlocal_control.pop()
    builder.builder.pop_error_handler()

    # Cleanup for if we leave except through normal control flow:
    # restore the saved exc_info information and continue propagating
    # the exception if it exists.
    builder.activate_block(cleanup_block)
    builder.call_c(restore_exc_info_op, [builder.read(old_exc, line)], line)
    builder.goto(exit_block)

    # Cleanup for if we leave except through a raised exception:
    # restore the saved exc_info information and continue propagating
    # the exception.
    builder.activate_block(double_except_block)
    builder.call_c(restore_exc_info_op, [builder.read(old_exc, line)], line)
    builder.call_c(keep_propagating_op, [], NO_TRACEBACK_LINE_NO)
    builder.add(Unreachable())

    # If present, compile the else body in the obvious way
    if else_body:
        builder.activate_block(else_block)
        else_body()
        builder.goto(exit_block)

    builder.activate_block(exit_block)

