
def associative_scan_autograd(combine_fn, xs, additional_inputs):
    num_xs = len(xs)
    num_additional_inputs = len(additional_inputs)

    if num_additional_inputs > 0:
        raise RuntimeError(
            "Associative_scan does currently not support gradients for lifted parameters!"
        )

    flat_out = AssociativeScanAutogradOp.apply(
        combine_fn,
        num_xs,
        num_additional_inputs,
        *(tuple(xs) + tuple(additional_inputs)),
    )
    return (*flat_out,)

