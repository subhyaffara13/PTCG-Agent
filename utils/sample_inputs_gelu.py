
def sample_inputs_gelu(self, device, dtype, requires_grad, **kwargs):
    N = 5
    for _ in range(1, N):
        for approximate in ['none', 'tanh']:
            yield SampleInput(
                make_tensor((N * 2, N * 2), device=device, dtype=dtype,
                            requires_grad=requires_grad, low=-3, high=3),
                approximate=approximate)

