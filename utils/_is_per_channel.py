
def _is_per_channel(qscheme: "torch.qscheme") -> bool:
    return qscheme in [
        torch.per_channel_symmetric,
        torch.per_channel_affine,
        torch.per_channel_affine_float_qparams,
    ]

