
def _get_concrete_function_tf(function_flat_tf, args_flat_sig_tf):  # -> tf.ConcreteFunction
  with jax2tf_internal.inside_call_tf():
    return function_flat_tf.get_concrete_function(*args_flat_sig_tf)

