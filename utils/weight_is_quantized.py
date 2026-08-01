
def weight_is_quantized(qconfig):
    """Given a qconfig, decide if the weight needs to be
    quantized or not
    """
    return weight_dtype(qconfig) in [
        torch.quint8,
        torch.qint8,
        torch.float16,
        torch.quint4x2,
        torch.uint8,
        torch.int8,
        torch.int16,
        torch.int32,
        torch.float8_e5m2,
        torch.float8_e4m3fn,
    ]

