
def _is_float_qparams(qscheme: "torch.qscheme") -> bool:
    return qscheme == torch.per_channel_affine_float_qparams

