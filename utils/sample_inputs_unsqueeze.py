
def sample_inputs_unsqueeze(op_info, device, dtype, requires_grad, **kwargs):
    for sample_input in sample_inputs_unary_dimwise(
        op_info, device, dtype, requires_grad, **kwargs
    ):
        yield sample_input

        last_dim_sample = _update_sample(sample_input, {"dim": -1})
        last_dim_sample.name = (
            f"{_describe_njt(last_dim_sample.input)}: add dim to the end"
        )
        # Tell the unbind reference how to canonicalize the dim kwargs
        # This is necessary because unsqueeze() allows for a dim after
        # the last dim to indicate an unsqueeze at the end.
        last_dim_sample.input._ndim = last_dim_sample.input.dim() + 1
        yield last_dim_sample

