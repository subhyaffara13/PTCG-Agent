
def to_theano(array, constant=False):
    """Convert a numpy array to ``theano.tensor.TensorType`` instance."""
    import theano  # type: ignore

    if has_array_interface(array):
        if constant:
            return theano.tensor.constant(array)

        return theano.tensor.TensorType(dtype=array.dtype, broadcastable=[False] * len(array.shape))()

    return array

