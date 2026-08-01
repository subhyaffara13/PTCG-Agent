
def error_inputs_masked_scatter(op_info, device, **kwargs):
    make_arg = partial(make_tensor, device=device, dtype=torch.float)
    for mask_dtype in [torch.float, torch.uint8]:
        yield ErrorInput(SampleInput(make_arg(1, 3), args=(torch.ones(1, 3, device=device, dtype=mask_dtype),
                                                           make_arg(3, 4))),
                         error_regex=r"masked_scatter_ only supports boolean masks")

