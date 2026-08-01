
def sample_inputs_upsample_aa(mode, self, device, dtype, requires_grad, **kwargs):
    N = 6
    C = 3
    H = 10
    W = 20
    S = 3
    L = 5

    input_tensor = make_tensor(torch.Size([N, C, H, W]), device=device, dtype=dtype, requires_grad=requires_grad)

    yield SampleInput(input_tensor, output_size=torch.Size([S, S]), align_corners=False, scale_factors=None)
    yield SampleInput(input_tensor, output_size=torch.Size([L, L]), align_corners=False, scale_factors=None)
    yield SampleInput(input_tensor, output_size=None, align_corners=False, scale_factors=[1.7, 0.9])
    yield SampleInput(input_tensor, output_size=None, align_corners=True, scale_factors=[0.8, 1.0])

    yield SampleInput(input_tensor, output_size=torch.Size([S, S]), align_corners=False, scales_h=None, scales_w=None)
    yield SampleInput(input_tensor, output_size=torch.Size([S, S]), align_corners=False, scales_h=1.7, scales_w=0.9)
    yield SampleInput(input_tensor, output_size=torch.Size([S, S]), align_corners=True, scales_h=1.7, scales_w=0.9)

