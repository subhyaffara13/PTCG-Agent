
def qdq_tensor(data, num_bits=4, group_size=32, scheme="asym", dtype="int", ratio=1.0):
    """Quant dequant tensor per group.

    Args:
        data : input weight
        num_bits (int, optional): num_bits. Defaults to 4.
        group_size (int, optional): how many elements share one scale/zp. Defaults to 4.
        scheme (str, optional): quantization scheme. Defaults to "asym".
        dtype (str, optional): data type. Defaults to "int".
        ratio (float, optional): percentile of clip. Defaults to 1.0.

    Returns:
        output: quant-dequant weight
    """
    org_shape = data.shape
    weight, scale, zp = quant_tensor(data, num_bits, group_size, scheme, dtype, ratio)
    return np.reshape(scale * (weight - zp), org_shape)

