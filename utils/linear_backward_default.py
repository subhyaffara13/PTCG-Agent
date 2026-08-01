
def linear_backward_default(func, *args, **kwargs):
    _, new_kwargs = normalize_function(  # type: ignore[misc]
        func, args=args, kwargs=kwargs, normalize_to_only_use_kwargs=True
    )

    inp = new_kwargs.pop("input")
    grad_output = new_kwargs.pop("grad_output")
    weight = new_kwargs.pop("weight")
    output_mask = new_kwargs.pop("output_mask")

    ds, dw, db = None, None, None
    check_ragged_dim_same(func, inp, "self", grad_output, "grad_output")
    if output_mask[0]:
        ds = NestedTensor(
            torch.matmul(grad_output._values, weight), **extract_kwargs(grad_output)
        )
    if output_mask[1]:
        # NB: Fold dims of values for input and grad_output to treat them as 2D. This
        # trick avoids materializing large intermediates and immediately reducing over
        # them via sum(). This is equivalent to computing:
        #     torch.matmul(grad_output._values.transpose(-2, -1), inp._values)
        # and then summing over the leading dimensions to get a 2D weight grad.
        grad_2d = grad_output._values.reshape(-1, weight.size(0))
        input_2d = inp._values.reshape(-1, weight.size(1))
        dw = torch.matmul(grad_2d.t(), input_2d)
    if output_mask[2]:
        # Sum over all but the last dim to get a 1D bias grad. We cannot
        # rely on the autograd engine to reduce for us, because returning a
        # tensor aliasing the input would violate the aten signature annotation
        reduce_dims = tuple(range(grad_output._values.ndim - 1))
        if reduce_dims == ():
            db = grad_output._values.clone()
        else:
            db = torch.sum(grad_output._values, reduce_dims, keepdim=False)
    return (ds, dw, db)

