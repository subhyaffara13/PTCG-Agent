
def sample_inputs_margin_ranking_loss(op_info, device, dtype, requires_grad, **kwargs):
    _make_tensor = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    shapes = (
        (),
        (S,),
        (S, S),
        (S, S, S),
    )

    margins = (0., 1.)
    reductions = ('sum', 'mean', 'none')

    for shape in shapes:
        for margin, reduction in product(margins, reductions):
            kwargs = {'margin': margin, 'reduction': reduction}
            yield SampleInput(_make_tensor(shape),
                              args=(_make_tensor(shape, requires_grad=False),
                                    _make_tensor(shape, requires_grad=False)),
                              kwargs=kwargs)

