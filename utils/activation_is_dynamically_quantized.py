
def activation_is_dynamically_quantized(qconfig):
    """Given a qconfig, decide if the activation needs to be
    dynamically quantized or not, this includes dynamically quantizing to
    quint8, qint8 and float16
    """
    _activation_dtype, _, activation_is_dynamic = get_qconfig_dtypes(qconfig)
    return activation_is_dynamic

