
def add_raise_exception_blocks_to_generator_class(builder: IRBuilder, line: int) -> None:
    """Add error handling blocks to a generator class.

    Generates blocks to check if error flags are set while calling the
    helper method for generator functions, and raises an exception if
    those flags are set.
    """
    cls = builder.fn_info.generator_class
    assert cls.exc_regs is not None
    exc_type, exc_val, exc_tb = cls.exc_regs

    # Check to see if an exception was raised.
    error_block = BasicBlock()
    ok_block = BasicBlock()
    comparison = builder.translate_is_op(exc_type, builder.none_object(), "is not", line)
    builder.add_bool_branch(comparison, error_block, ok_block)

    builder.activate_block(error_block)
    builder.call_c(raise_exception_with_tb_op, [exc_type, exc_val, exc_tb], line)
    builder.add(Unreachable())
    builder.goto_and_activate(ok_block)

