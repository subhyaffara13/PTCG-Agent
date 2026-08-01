
def weight_is_statically_quantized(qconfig):
    """Given a qconfig, decide if the weight needs to be statically
    quantized or not
    """
    return weight_dtype(qconfig) in [torch.quint8, torch.qint8, torch.uint8, torch.int8]

