
def sample_inputs_lerp(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)

    # no broadcast
    yield SampleInput(make_arg((S, S)), make_arg((S, S)), 0.4)
    # broadcast rhs
    yield SampleInput(make_arg((S, S)), make_arg((S,)), 0.4)
    # scalar tensor
    yield SampleInput(make_arg(()), make_arg(()), 0.4)
    # broadcast rhs scalar-tensor
    yield SampleInput(make_arg((S, S)), make_arg(()), 0.4)
    # broadcast rhs with weight tensor
    yield SampleInput(make_arg((S, S)), make_arg((S,)), make_arg((S, S)))
    # broadcast rhs and weight tensor
    yield SampleInput(make_arg((S, S)), make_arg((S, 1)), make_arg((S,)))
    # broadcast lhs
    yield SampleInput(make_arg((S,)), make_arg((S, S)), 0.4).with_metadata(broadcasts_input=True)
    # scalar broadcast_lhs
    yield SampleInput(make_arg(()), make_arg((S, S)), 0.4).with_metadata(broadcasts_input=True)
    # broadcast all
    yield SampleInput(make_arg((S, 1)), make_arg((S, S)), 0.4).with_metadata(broadcasts_input=True)
    # tensor broadcast all
    yield SampleInput(make_arg((S, 1)), make_arg((S, S)), make_arg((S, 1))).with_metadata(
        broadcasts_input=True)
    # no broadcast with weight tensor
    yield SampleInput(make_arg((S, S)), make_arg((S, S)), make_arg((S, S)))
    # broadcast lhs with weight tensor
    yield SampleInput(make_arg((S,)), make_arg((S, S)), make_arg((S, S))).with_metadata(
        broadcasts_input=True)
    # broadcast lhs and weight tensor
    yield SampleInput(make_arg((S,)), make_arg((S, S, S)), make_arg((S, S))).with_metadata(
        broadcasts_input=True)
    # broadcast lhs and weight tensor variant
    yield SampleInput(make_arg((S, S)), make_arg((S, S, S)), make_arg((S,))).with_metadata(
        broadcasts_input=True)

    if dtype.is_complex:
        # no broadcast
        yield SampleInput(make_arg((S, S)), make_arg((S, S)), 0.4j)
        yield SampleInput(make_arg((S, S)), make_arg((S, S)), 1.2 + 0.1j)
        # broadcast rhs
        yield SampleInput(make_arg((S, S)), make_arg((S,)), 0.4j)
        yield SampleInput(make_arg((S, S)), make_arg((S, S)), 5.4 + 9j)
        # scalar tensor
        yield SampleInput(make_arg(()), make_arg(()), 0.4j)
        yield SampleInput(make_arg(()), make_arg(()), 6.1 + 0.004j)
        # broadcast rhs scalar-tensor
        yield SampleInput(make_arg((S, S)), make_arg(()), 0.4j)
        yield SampleInput(make_arg((S, S)), make_arg(()), 1 + 2j)

