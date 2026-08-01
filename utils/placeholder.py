
def placeholder(field_type, required=False):
  """Defines an entry in a ConfigDict that has no value yet.

  Example::

    config = configdict.create(
        batch_size = configdict.placeholder(int),
        frame_shape = configdict.placeholder(tf.TensorShape))

  Args:
    field_type: type of value.
    required: If True, the placeholder will raise an error on access if the
         underlying value hasn't been set.

  Returns:
    A `FieldReference` with value None and the given type.
  """
  return FieldReference(None, field_type=field_type, required=required)

