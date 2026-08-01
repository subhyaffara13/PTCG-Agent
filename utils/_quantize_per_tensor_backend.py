
def _quantize_per_tensor_backend(x, scale, zero_point):
    y = torch.round(x / scale) + zero_point
    y = torch.clamp(y, 0, 255).to(torch.uint8)
    return y

