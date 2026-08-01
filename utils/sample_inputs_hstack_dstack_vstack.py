
def sample_inputs_hstack_dstack_vstack(op_info, device, dtype, requires_grad, **kwargs):
    make_arg = partial(make_tensor, dtype=dtype, device=device, requires_grad=requires_grad)
    tensor_shapes = (
        # First Tensor being 1-D is special
        # case for hstack
        ((S,), (S,), (S,)),
        ((S, S), (S, S), (S, S)),
    )
    for s1, s2, s3 in tensor_shapes:
        tensors = (make_arg(s1,), make_arg(s2,), make_arg(s3))
        yield SampleInput(tensors)

