
def sample_inputs_loss(op_info, device, dtype, requires_grad, **kwargs):
    rhs_requires_grad = kwargs.get('rhs_requires_grad', requires_grad)
    _make_tensor = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    # Although most losses also support the reduce and size_average combination instead of reduce, the former is
    # deprecated since 0.4.1 and thus is not tested
    shapes_and_kwargs = (
        ((), None),
        ((S,), dict(reduction="mean")),
        ((S,), dict(reduction="sum")),
        ((S,), dict(reduction="none")),
        ((S, S), None),
        ((S, S, S), None),
    )

    for shape, kwargs in shapes_and_kwargs:
        yield SampleInput(_make_tensor(shape),
                          args=(_make_tensor(shape, requires_grad=rhs_requires_grad),),
                          kwargs=kwargs)

