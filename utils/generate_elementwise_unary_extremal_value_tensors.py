
def generate_elementwise_unary_extremal_value_tensors(
    op, *, device, dtype, requires_grad=False
):
    for sample in generate_elementwise_binary_extremal_value_tensors(
        op, device=device, dtype=dtype, requires_grad=requires_grad
    ):
        yield SampleInput(
            sample.input, kwargs=op.sample_kwargs(device, dtype, sample.input)[0]
        )

