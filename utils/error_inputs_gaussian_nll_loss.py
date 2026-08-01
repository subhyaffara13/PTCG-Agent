
def error_inputs_gaussian_nll_loss(op_info, device, **kwargs):
    _make = partial(make_tensor, device=device, dtype=torch.float32)

    # invalid reduction value
    yield ErrorInput(SampleInput(_make(10, 2, 3), _make(10, 2, 3), _make((10, 2, 3), low=0), reduction="abc"),
                     error_type=ValueError, error_regex="abc is not valid")

    # var is of incorrect shape
    yield ErrorInput(SampleInput(_make(10, 2, 3), _make(10, 2, 3), _make((10, 2, 2), low=0)),
                     error_type=ValueError, error_regex="var is of incorrect size")

    # target is of incorrect shape
    yield ErrorInput(SampleInput(_make(10, 2, 3), _make(10, 2, 2), _make((10, 2, 3), low=0)),
                     error_type=RuntimeError,
                     error_regex=(r"The size of tensor a \(3\) must match the size of tensor b \(2\) "
                                  r"at non-singleton dimension 2"))

