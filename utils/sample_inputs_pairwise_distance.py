
def sample_inputs_pairwise_distance(op_info, device, dtype, requires_grad, **kwargs):
    make = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    shape = (3,)
    batched_shape = (2, *shape)
    shapes_and_kwargs = [
        (shape, None),
        (batched_shape, None),
        (shape, dict(keepdim=True)),
        (batched_shape, dict(keepdim=True)),
        (shape, dict(p=5.0)),
        (shape, dict(p=-1.0)),
        (shape, dict(eps=1.0)),
    ]

    return (
        SampleInput(make(shape), args=(make(shape),), kwargs=kwargs) for shape, kwargs in shapes_and_kwargs
    )

