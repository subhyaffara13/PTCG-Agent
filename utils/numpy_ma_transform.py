
def numpy_ma_transform() -> nodes.Module:
    """
    Infer the call of various numpy.ma functions.

    :param node: node to infer
    :param context: inference context
    """
    return parse(
        """
    import numpy.ma
    def masked_where(condition, a, copy=True):
        return numpy.ma.masked_array(a, mask=[])

    def masked_invalid(a, copy=True):
        return numpy.ma.masked_array(a, mask=[])
    """
    )

