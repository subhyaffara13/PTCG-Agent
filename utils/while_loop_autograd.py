
def while_loop_autograd(cond_fn, body_fn, operands, additional_inputs):
    return WhileLoopAutogradOp.apply(
        cond_fn,
        body_fn,
        len(operands),
        len(additional_inputs),
        *operands,
        *additional_inputs,
    )

