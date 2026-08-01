
def error_inputs_item(op, device, **kwargs):
    make_arg = partial(make_tensor, dtype=torch.float32, device=device, requires_grad=False)

    cases = (
        (M),
        ((S,)),
        (S, S),
        (S, M, L),
    )

    for shape in cases:
        yield ErrorInput(
            SampleInput(make_arg(shape)), error_type=RuntimeError,
            error_regex="elements cannot be converted to Scalar")

