
def jax_to_ir(fn, input_shapes, *, constants=None, format):
  """Converts a JAX function to a serialized ir and a debug txt dump.

  Args:
    fn: Function to convert.
    input_shapes: List of tuples (arg name, jax.core.ShapedArray),
      indicating the shapes of the arguments to fn.  The order of parameters in
      the resulting XLA program will match the order in this list.
    constants: Dict mapping function argument name to a Python value.  Specified
      arguments these values as compile-time constants.
    format: Which IR format to use. Supported values are 'HLO' and 'TF'.

  Returns:
    A tuple of (compiler_suitable_ir, human_readable_ir).
  """
  if not constants:
    constants = {}

  overlapping_args = {arg_name for arg_name, _ in input_shapes} & set(
      constants.keys())
  if overlapping_args:
    raise ValueError(
        'Arguments appear in both `input_shapes` and `constants`: %s' %
        ', '.join(sorted(overlapping_args)))

  # TODO(tomhennigan): Ideally we could avoid creating actual values here.
  args = [jnp.zeros(s.shape, s.dtype) for _, s in input_shapes]

  # Curry `constants` into the function.
  fn_curried = functools.partial(fn, **constants)

  # Wrapper that takes in args in the order of `input_shapes` and converts them
  # to kwargs for calling `fn`.
  def ordered_wrapper(*args):
    arg_names = [arg_name for arg_name, _ in input_shapes]
    return fn_curried(**dict(zip(arg_names, args)))

  if format == 'HLO':
    comp = jax.jit(ordered_wrapper).lower(*args).compiler_ir('hlo')
    assert comp is not None
    serialized_proto = comp.as_serialized_hlo_module_proto()
    debug_txt = comp.as_hlo_text()
  else:
    assert format == 'TF'
    if tf is None:
      raise ValueError(
          'Conversion to TF graph requires TensorFlow to be installed.')
    if jax2tf is None:
      raise ValueError(
          'Conversion to TF graph requires jax.experimental.jax2tf to be importable.')

    f = jax2tf.convert(ordered_wrapper)
    f = tf_wrap_with_input_names(f, input_shapes)
    f = tf.function(f, autograph=False)
    g = f.get_concrete_function(*args).graph.as_graph_def()
    serialized_proto = g.SerializeToString()
    debug_txt = str(g)

  return serialized_proto, debug_txt

