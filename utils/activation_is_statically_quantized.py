
def activation_is_statically_quantized(qconfig):
    """Given a qconfig, decide if the activation needs to be
    quantized or not, this includes quantizing to quint8, qint8 and qint32 and float16
    """
    return activation_dtype(qconfig) in [
        torch.quint8,
        torch.qint8,
        torch.qint32,
        torch.float16,
        torch.uint8,
        torch.int8,
        torch.int16,
        torch.int32,
        torch.float8_e5m2,
        torch.float8_e4m3fn,
    ] and (not activation_is_dynamically_quantized(qconfig))

