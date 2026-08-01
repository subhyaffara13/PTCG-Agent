
def error_inputs_hstack_dstack_vstack(op, device):
    make_arg = partial(make_tensor, dtype=torch.int32, device=device, requires_grad=False)
    tensor_shapes = (
        ((S,), (S, S, S, S), (S,)),
    )
    for s1, s2, s3 in tensor_shapes:
        tensors = (make_arg(s1,), make_arg(s2,), make_arg(s3))
        # Different dimension tensor
        yield ErrorInput(SampleInput(tensors), error_regex="Tensors must have same number of dimensions")

    # empty tensor list
    yield ErrorInput(SampleInput(()), error_regex="expects a non-empty TensorList")

