
def sample_inputs_cov(op_info, device, dtype, requires_grad, **kwargs):
    for t in _generate_correlation_inputs(device, dtype, requires_grad):
        yield SampleInput(t)
        num_observations = t.numel() if t.ndimension() < 2 else t.size(1)
        fweights = make_tensor((num_observations,), dtype=torch.int, device=device, low=1, high=10)
        aweights = make_tensor((num_observations,), dtype=torch.float, device=device, low=0, high=1, requires_grad=requires_grad)
        for correction, fw, aw in product(range(num_observations), [None, fweights], [None, aweights]):
            yield SampleInput(t.clone().requires_grad_(requires_grad),
                              correction=correction, fweights=fw, aweights=aw)

