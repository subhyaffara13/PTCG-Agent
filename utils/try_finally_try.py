
def try_finally_try(
    builder: IRBuilder,
    err_handler: BasicBlock,
    return_entry: BasicBlock,
    main_entry: BasicBlock,
    try_body: GenFunc,
) -> Register | AssignmentTarget | None:
    # Compile the try block with an error handler
    control = TryFinallyNonlocalControl(return_entry)
    builder.builder.push_error_handler(err_handler)

    builder.nonlocal_control.append(control)
    builder.goto_and_activate(BasicBlock())
    try_body()
    builder.goto(main_entry)
    builder.nonlocal_control.pop()
    builder.builder.pop_error_handler()

    return control.ret_reg

