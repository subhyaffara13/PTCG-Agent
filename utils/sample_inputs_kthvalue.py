
def sample_inputs_kthvalue(op_info, device, dtype, requires_grad, **kwargs):
    def _tensor(shape, dtype=dtype, low=None, high=None):
        return make_tensor(shape, dtype=dtype, device=device, low=low, high=high, requires_grad=requires_grad)

    test_cases = [
        ((S, S, S), (2,)),
        ((S, S, S), (2, 1,)),
        ((S, S, S), (2, -1,)),
        ((S, S, S), (2, 1, True,)),
        ((S, S, S), (2, -1, True,)),
        ((S,), (2, 0,)),
        ((S,), (2, 0, True,)),
        ((), (1,)),
        ((), (1, 0,)),
        ((), (1, 0, True)),
    ]

    yield from (SampleInput(_tensor(tensor), *args) for tensor, args in test_cases)

