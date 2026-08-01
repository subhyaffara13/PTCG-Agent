
def activation_is_int8_quantized(qconfig):
    """Given a qconfig, decide if the activation needs to be
    quantized to int8 or not, this includes quantizing to quint8, qint8
    """
    return activation_dtype(qconfig) in [
        torch.quint8,
        torch.qint8,
        torch.uint8,
        torch.int8,
    ]

