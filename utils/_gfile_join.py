
def _gfile_join(a, b):
    # The join API is different between tensorboard's TF stub and TF:
    # https://github.com/tensorflow/tensorboard/issues/6080
    # We need to try both because `tf` may point to either the stub or the real TF.
    if _HAS_GFILE_JOIN:
        return tf.io.gfile.join(a, b)
    else:
        fs = tf.io.gfile.get_filesystem(a)
        return fs.join(a, b)

