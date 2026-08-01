
def _get_tensorflow_and_device():
    global _CACHED_TF_DEVICE

    if _CACHED_TF_DEVICE is None:
        import tensorflow as tf  # type: ignore

        try:
            eager = tf.executing_eagerly()
        except AttributeError:
            try:
                eager = tf.contrib.eager.in_eager_mode()
            except AttributeError:
                eager = False

        device = tf.test.gpu_device_name()
        if not device:
            device = "cpu"

        _CACHED_TF_DEVICE = tf, device, eager

    return _CACHED_TF_DEVICE

