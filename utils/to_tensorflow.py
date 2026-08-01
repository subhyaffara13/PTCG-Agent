
def to_tensorflow(array, constant=False):
    """Convert a numpy array to a ``tensorflow.placeholder`` instance."""
    tf, device, eager = _get_tensorflow_and_device()

    if eager:
        if has_array_interface(array):
            with tf.device(device):
                return tf.convert_to_tensor(array)

        return array

    if has_array_interface(array):
        if constant:
            return tf.convert_to_tensor(array)

        return tf.placeholder(array.dtype, array.shape)

    return array

