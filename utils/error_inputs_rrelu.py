
def error_inputs_rrelu(op_info, device, **kwargs):
    input = make_tensor((S, S), device=device, dtype=torch.float32)
    yield ErrorInput(SampleInput(input, kwargs={'lower': 0.3, 'upper': 0.1}),
                     error_regex='Lower bound should be less than or equal to the upper bound')

