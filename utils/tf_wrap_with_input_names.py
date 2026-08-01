
def tf_wrap_with_input_names(f, input_shapes):
  def wrapper(*args):
    assert tf is not None  # checked in caller
    args = tuple(
        tf.identity(a, name=name) for a, (name, _) in zip(args, input_shapes))
    # NOTE: Output names already set via `jax2tf.convert(..)`.
    return f(*args)
  return wrapper

