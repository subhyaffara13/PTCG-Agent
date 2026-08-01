
def generate_elementwise_unary_large_value_tensors(
    op, *, device, dtype, requires_grad=False
):
    for sample in generate_elementwise_binary_large_value_tensors(
        op, device=device, dtype=dtype, requires_grad=requires_grad
    ):
        a = _filter_unary_elementwise_tensor(sample.input, op=op)
        yield SampleInput(sample.input, kwargs=op.sample_kwargs(device, dtype, a)[0])

