
def dequantize_convertops(blocks, scales):
    dequantized = convert_moe_packed_tensors(blocks, scales)
    return torch.nn.Parameter(dequantized)

