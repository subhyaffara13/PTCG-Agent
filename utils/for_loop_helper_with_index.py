from typing import Callable

def for_loop_helper_with_index(
    builder: IRBuilder,
    index: Lvalue,
    expr: Expression,
    expr_reg: Value,
    body_insts: Callable[[Value], None],
    line: int,
    length: Value,
) -> None:
    """Generate IR for a sequence iteration.

    This function only works for sequence type. Compared to for_loop_helper,
    it would feed iteration index to body_insts.

    Args:
        index: the loop index Lvalue
        expr: the expression to iterate over
        body_insts: a function that generates the body of the loop.
                    It needs a index as parameter.
    """
    assert is_sequence_rprimitive(expr_reg.type) or isinstance(expr_reg.type, RVec), (
        expr_reg,
        expr_reg.type,
    )
    target_type = builder.get_sequence_type(expr)

    body_block = BasicBlock()
    step_block = BasicBlock()
    exit_block = BasicBlock()
    condition_block = BasicBlock()

    for_gen = ForSequence(builder, index, body_block, exit_block, line, False)
    for_gen.init(expr_reg, target_type, reverse=False, length=length)

    builder.push_loop_stack(step_block, exit_block)

    if isinstance(length, Integer) and length.value > 0:
        builder.goto(body_block)
        builder.activate_block(condition_block)
    else:
        builder.goto_and_activate(condition_block)

    for_gen.gen_condition()

    builder.activate_block(body_block)
    for_gen.begin_body()
    body_insts(builder.read(for_gen.index_target, line))

    builder.goto_and_activate(step_block)
    for_gen.gen_step()
    builder.goto(condition_block)

    for_gen.add_cleanup(exit_block)
    builder.pop_loop_stack()

    builder.activate_block(exit_block)

