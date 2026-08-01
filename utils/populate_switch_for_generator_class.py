
def populate_switch_for_generator_class(builder: IRBuilder) -> None:
    cls = builder.fn_info.generator_class
    line = builder.fn_info.fitem.line

    builder.activate_block(cls.switch_block)
    for label, true_block in enumerate(cls.continuation_blocks):
        false_block = BasicBlock()
        comparison = builder.binary_op(cls.next_label_reg, Integer(label), "==", line)
        builder.add_bool_branch(comparison, true_block, false_block)
        builder.activate_block(false_block)

    builder.add(RaiseStandardError(RaiseStandardError.STOP_ITERATION, None, line))
    builder.add(Unreachable())

