
def is_per_channel(qscheme):
    return qscheme in [
        torch.per_channel_affine,
        torch.per_channel_affine_float_qparams,
        torch.per_channel_symmetric,
    ]

