
def sample_inputs_multilabel_soft_margin_loss(op_info, device, dtype, requires_grad, **kwargs):
    _make_tensor = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    shapes = (
        (S,),
        (S, S),
    )

    for shape in shapes:
        # Produce one with weight and one without.
        yield SampleInput(_make_tensor(shape), args=(_make_tensor(shape, requires_grad=False),), kwargs={})
        yield SampleInput(_make_tensor(shape), args=(_make_tensor(shape, requires_grad=False),),
                          kwargs={'weight': _make_tensor(shape, requires_grad=False)})

