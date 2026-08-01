
def _dequantize_per_tensor_backend(y, scale, zero_point):
    x = scale * (y.to(torch.float32) - zero_point)
    return x

