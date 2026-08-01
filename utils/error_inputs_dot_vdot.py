
def error_inputs_dot_vdot(op_info, device, is_ref=False, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=torch.float32)

    yield ErrorInput(SampleInput(make_input(1), args=(make_input(3, dtype=torch.float16),)),
                     error_regex='dot : expected both vectors to have same dtype')
    yield ErrorInput(SampleInput(make_input(1, 1), args=(make_input(3),)),
                     error_regex='1D tensors expected')
    yield ErrorInput(SampleInput(make_input(9), args=(make_input(3),)),
                     error_regex='inconsistent tensor size')
    if device != "cpu" and not is_ref:
        yield ErrorInput(SampleInput(make_input(3), args=(make_input(3, device="cpu"),)),
                         error_regex='Expected all tensors to be on the same device')

