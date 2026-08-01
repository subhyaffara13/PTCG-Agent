
def sample_inputs_resize_ops(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device)
    cases = (((S, S, S), (S * S, S)),
             ((), ()),
             ((), (1, 1, 1)),
             )

    for shape, args_or_shape in cases:
        # Update `args` based on operator
        if op_info.name == 'resize_':
            # resize_ takes shape/tuple of ints,
            args = (args_or_shape, )
        elif op_info.name == 'resize_as_':
            # resize_as_ takes another tensor
            args = (make_arg(shape, requires_grad=False), )  # type:ignore[assignment]
        else:
            raise ValueError("sample_inputs_resize_ops is being used with incorrect operator")

        yield SampleInput(make_arg(shape, requires_grad=requires_grad), args=args)

