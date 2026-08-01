
def transform_try_finally_stmt_async(
    builder: IRBuilder, try_body: GenFunc, finally_body: GenFunc, line: int = -1
) -> None:
    """Async-aware try/finally handling for when finally contains await.

    This version uses a modified approach that preserves exceptions across await."""

    # We need to handle returns properly, so we'll use TryFinallyNonlocalControl
    # to track return values, similar to the regular try/finally implementation

    err_handler, main_entry, return_entry, finally_entry = (
        BasicBlock(),
        BasicBlock(),
        BasicBlock(),
        BasicBlock(),
    )

    # Track if we're returning from the try block
    control = TryFinallyNonlocalControl(return_entry)
    builder.builder.push_error_handler(err_handler)
    builder.nonlocal_control.append(control)
    builder.goto_and_activate(BasicBlock())
    try_body()
    builder.goto(main_entry)
    builder.nonlocal_control.pop()
    builder.builder.pop_error_handler()
    ret_reg = control.ret_reg

    # Normal case - no exception or return
    builder.activate_block(main_entry)
    builder.goto(finally_entry)

    # Return case
    builder.activate_block(return_entry)
    builder.goto(finally_entry)

    # Exception case - need to catch to clear the error indicator
    builder.activate_block(err_handler)
    # Catch the error to clear Python's error indicator
    builder.call_c(error_catch_op, [], line)
    # We're not going to use old_exc since it won't survive await
    # The exception is now in sys.exc_info()
    builder.goto(finally_entry)

    # Finally block
    builder.activate_block(finally_entry)

    # Execute finally body
    finally_body()

    # After finally, we need to handle exceptions carefully:
    # 1. If finally raised a new exception, it's in the error indicator - let it propagate
    # 2. If finally didn't raise, check if we need to reraise the original from sys.exc_info()
    # 3. If there was a return, return that value
    # 4. Otherwise, normal exit

    # First, check if there's a current exception in the error indicator
    # (this would be from the finally block)
    no_current_exc = builder.call_c(no_err_occurred_op, [], line)
    finally_raised = BasicBlock()
    check_original = BasicBlock()
    builder.add(Branch(no_current_exc, check_original, finally_raised, Branch.BOOL))

    # Finally raised an exception - let it propagate naturally
    builder.activate_block(finally_raised)
    builder.call_c(keep_propagating_op, [], NO_TRACEBACK_LINE_NO)
    builder.add(Unreachable())

    # No exception from finally, check if we need to handle return or original exception
    builder.activate_block(check_original)

    # Check if we have a return value
    if ret_reg:
        return_block, check_old_exc = BasicBlock(), BasicBlock()
        builder.add(
            Branch(
                builder.read(ret_reg, line, allow_error_value=True),
                check_old_exc,
                return_block,
                Branch.IS_ERROR,
            )
        )

        builder.activate_block(return_block)
        builder.nonlocal_control[-1].gen_return(builder, builder.read(ret_reg, line), line)

        builder.activate_block(check_old_exc)

    # Check if we need to reraise the original exception from sys.exc_info
    exc_info = builder.call_c(get_exc_info_op, [], line)
    exc_type = builder.add(TupleGet(exc_info, 0, line))

    # Check if exc_type is None
    none_obj = builder.none_object()
    has_exc = builder.binary_op(exc_type, none_obj, "is not", line)

    reraise_block, exit_block = BasicBlock(), BasicBlock()
    builder.add(Branch(has_exc, reraise_block, exit_block, Branch.BOOL))

    # Reraise the original exception
    builder.activate_block(reraise_block)
    builder.call_c(reraise_exception_op, [], NO_TRACEBACK_LINE_NO)
    builder.add(Unreachable())

    # Normal exit
    builder.activate_block(exit_block)

