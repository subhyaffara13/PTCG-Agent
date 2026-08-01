
def sample_inputs_normal_tensor_second(self, device, dtype, requires_grad, **kwargs):
    yield SampleInput(1.6, 0.3, [2, 3], dtype=dtype, device=device)
    yield SampleInput(1.6, 0.3, [2, 2, 2], dtype=dtype, layout=torch.strided, device=device)
    yield SampleInput(2.7, make_tensor([4, 3], dtype=dtype, device=device, low=0, high=None, requires_grad=requires_grad))

