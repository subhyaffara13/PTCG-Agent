
def error_inputs_logcumsumexp(op_info, device, **kwargs):
    dim = 3
    srcs = [torch.randn(5, 2, device=device), torch.randn(0, 2, device=device)]
    for src in srcs:
        yield ErrorInput(SampleInput(src, args=(dim,)),
                         error_type=IndexError,
                         error_regex='Dimension out of range')

