
def sample_inputs_as_strided_partial_views(op_info, device, dtype, requires_grad, **kwargs):
    def make_arg():
        base = make_tensor((20,), device=device, dtype=dtype)
        return base[5:15].requires_grad_(requires_grad)

    # as_strided on offset, partial views
    yield SampleInput(make_arg(), (2, 2), (1, 2))
    yield SampleInput(make_arg(), (2, 2), (1, 2), storage_offset=0)
    yield SampleInput(make_arg(), (2, 2), (1, 2), storage_offset=10)

