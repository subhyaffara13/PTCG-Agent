
def _frombuffer(buf, dtype, shape, order, axis_order=None):
    array = frombuffer(buf, dtype=dtype)
    if order == 'K' and axis_order is not None:
        return array.reshape(shape, order='C').transpose(axis_order)
    return array.reshape(shape, order=order)

