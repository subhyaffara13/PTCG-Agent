
def error_inputs_bernoulli(op_info, device, **kwargs):
    # more than one element of the written-to tensor refers to a single memory location
    x = torch.rand((1,), device=device).expand((6,))
    err_msg = 'unsupported operation'
    yield ErrorInput(SampleInput(torch.rand_like(x), kwargs={'out': x}),
                     error_regex=err_msg)

