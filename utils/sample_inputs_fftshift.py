
def sample_inputs_fftshift(op_info, device, dtype, requires_grad, **kwargs):
    def mt(shape, **kwargs):
        return make_tensor(
            shape, device=device, dtype=dtype, requires_grad=requires_grad, **kwargs
        )

    yield SampleInput(mt((9, 10)))
    yield SampleInput(mt((50,)), kwargs=dict(dim=0))
    yield SampleInput(mt((5, 11)), kwargs=dict(dim=(1,)))
    yield SampleInput(mt((5, 6)), kwargs=dict(dim=(0, 1)))
    yield SampleInput(mt((5, 6, 2)), kwargs=dict(dim=(0, 2)))

