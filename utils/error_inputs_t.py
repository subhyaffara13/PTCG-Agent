
def error_inputs_T(self, device, has_ndims_error=False):
    make_arg = partial(make_tensor, device=device, dtype=torch.float32)

    # Deprecated behavior in regular PyTorch, but throws an error in primTorch:
    # https://github.com/pytorch/pytorch/issues/86968
    if has_ndims_error:
        # ndims == 1
        yield ErrorInput(SampleInput(make_arg(M)),
                         error_regex=(r'The use of `x\.T` on tensors of dimension other than 0 or 2 '
                                      r'to reverse their shape is not supported\.'))

        # ndims > 2
        yield ErrorInput(SampleInput(make_arg(M, S, L)),
                         error_regex=(r'The use of `x\.T` on tensors of dimension other than 0 or 2 '
                                      r'to reverse their shape is not supported\.'))


def error_inputs_t(op_info, device, **kwargs):
    yield ErrorInput(
        SampleInput(torch.randn(2, 3, 4, 5, device=device)),
        error_regex="expects a tensor with <= 2",
    )

