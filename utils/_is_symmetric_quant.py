
def _is_symmetric_quant(qscheme: "torch.qscheme") -> bool:
    return qscheme in [torch.per_tensor_symmetric, torch.per_channel_symmetric]

