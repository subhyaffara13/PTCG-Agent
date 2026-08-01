
def emit_yield(builder: IRBuilder, val: Value, line: int) -> Value:
    retval = builder.coerce(val, builder.ret_types[-1], line)

    cls = builder.fn_info.generator_class
    # Create a new block for the instructions immediately following the yield expression, and
    # set the next label so that the next time '__next__' is called on the generator object,
    # the function continues at the new block.
    next_block = BasicBlock()
    next_label = len(cls.continuation_blocks)
    cls.continuation_blocks.append(next_block)
    builder.assign(cls.next_label_target, Integer(next_label), line)
    builder.add(Return(retval, yield_target=next_block))
    builder.activate_block(next_block)

    add_raise_exception_blocks_to_generator_class(builder, line)

    assert cls.send_arg_reg is not None
    return cls.send_arg_reg

