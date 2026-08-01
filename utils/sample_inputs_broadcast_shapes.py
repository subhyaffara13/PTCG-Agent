
def sample_inputs_broadcast_shapes(op, device, dtype, requires_grad, **kwargs):
    shapes = (
        ((), ()),
        ((S,), ()),
        ((S, 1), (S,)),
        ((S, 1), S),
        ((M, S), ()),
        ((S, M, S), (M, S)),
        ((S, M, S), (S, M, S)),
        ((M, 1, S), (M, S)),
        ((M, 1, S), (1, M, S)),
        ((0, 1, 3), (0, 10, 3))
    )

    for shape in shapes:
        inp, *arg0 = shape
        yield SampleInput(inp, args=tuple(arg0))

