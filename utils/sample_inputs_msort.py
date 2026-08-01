
def sample_inputs_msort(op_info, device, dtype, requires_grad, **kwargs):
    def apply_grad(t):
        if dtype in floating_types_and(torch.float16, torch.bfloat16):
            t.requires_grad_(requires_grad)

    def large_1d_unique(dtype, device):
        res = torch.randperm(L * L * L, dtype=torch.int64, device=device)
        res = res.to(dtype)
        apply_grad(res)
        return res

    # Test case for large tensor.
    yield SampleInput(large_1d_unique(dtype, device))

    yield SampleInput(make_tensor((S, M, S), dtype=dtype, device=device,
                                  low=None, high=None,
                                  requires_grad=requires_grad))

