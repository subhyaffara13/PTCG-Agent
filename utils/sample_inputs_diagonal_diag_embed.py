
def sample_inputs_diagonal_diag_embed(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(
        make_tensor, dtype=dtype, device=device, requires_grad=requires_grad
    )

    # Shapes for 2D Tensors
    shapes_2d = ((S, S), (3, 5), (5, 3))

    # Shapes for 3D Tensors
    shapes_3d = ((S, S, S),)

    kwargs_2d = ({}, dict(offset=2), dict(offset=2), dict(offset=1))
    kwargs_3d = (
        dict(offset=1, dim1=1, dim2=2),
        dict(offset=2, dim1=0, dim2=1),
        dict(offset=-2, dim1=0, dim2=1),
    )

    for shape, kwarg in chain(
        product(shapes_2d, kwargs_2d), product(shapes_3d, kwargs_3d)
    ):
        yield SampleInput(make_arg(shape), kwargs=kwarg)

