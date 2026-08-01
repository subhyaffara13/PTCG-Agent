
def reference_inputs_diagonal_diag_embed(op_info, device, dtype, requires_grad, **kwargs):
    yield from sample_inputs_diagonal_diag_embed(
        op_info, device, dtype, requires_grad, **kwargs)

    make_arg = partial(
        make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)

    shapes1d = ((0,), (1,))
    shapes2d = ((L, M),)
    shapes3d = ((L, M, S),)

    kwargs1d = {}

    kwargs2d = (
        # dim1 > dim2 is allowed
        dict(dim1=1, dim2=0),
        # negative dims are allowed
        dict(dim1=-2, dim2=-1),
        # one dim negative and the other nonnegative is allowed
        dict(dim1=-1, dim2=0),
        # out of bounds offset should return an empty tensor in diagonal and
        # offset the diagonal in diag_embed
        dict(offset=100),
    )

    kwargs3d = kwargs2d + (
        # make sure we can use non-sequential dims
        dict(offset=-1, dim1=0, dim2=2),
    )

    samples1d = product(shapes1d, kwargs1d)
    samples2d = product(shapes2d, kwargs2d)
    samples3d = product(shapes3d, kwargs3d)

    for shape, kwargs in chain(samples1d, samples2d, samples3d):
        if 'diagonal' in op_info.name:
            # these are error inputs for diagonal
            if shape in ((0,), (1,)):
                continue
        yield SampleInput(input=make_arg(shape), kwargs=kwargs)

