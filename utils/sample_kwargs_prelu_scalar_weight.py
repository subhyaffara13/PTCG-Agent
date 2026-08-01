
def sample_kwargs_prelu_scalar_weight(device, dtype, input):
    weight = torch.rand((), device=device, dtype=dtype)
    # NumPy does not support bfloat16, so we default to float32 (only for NumPy) in that case
    if dtype == torch.bfloat16:
        weight_cpu = weight.to(dtype=torch.float32, device="cpu")
    else:
        weight_cpu = weight.cpu()
    np_weight = weight_cpu.numpy()
    return ({'weight': weight}, {'weight': np_weight})

