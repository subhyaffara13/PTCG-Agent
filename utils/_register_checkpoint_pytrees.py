
def _register_checkpoint_pytrees():
  """Registers TF custom container types as pytrees."""
  m = tf.Module()
  # The types here are automagically changed by TensorFlow's checkpointing
  # infrastructure.
  m.a = (tf.Module(), tf.Module())  # pyrefly: ignore [missing-attribute]
  m.b = [tf.Module(), tf.Module()]  # pyrefly: ignore [missing-attribute]
  m.c = {"a": tf.Module()}  # pyrefly: ignore [missing-attribute]
  tuple_wrapper = type(m.a)  # pyrefly: ignore [missing-attribute]
  list_wrapper = type(m.b)  # pyrefly: ignore [missing-attribute]
  dict_wrapper = type(m.c)  # pyrefly: ignore [missing-attribute]

  # TF AutoTrackable swaps container types out for wrappers.
  assert tuple_wrapper is not tuple
  assert list_wrapper is not list
  assert dict_wrapper is not dict

  jax.tree_util.register_pytree_node(tuple_wrapper, lambda xs:
                                     (tuple(xs), None), lambda _, xs: tuple(xs))

  jax.tree_util.register_pytree_node(list_wrapper, lambda xs: (tuple(xs), None),
                                     lambda _, xs: list(xs))

  jax.tree_util.register_pytree_node(
      dict_wrapper,
      lambda s: (tuple(s.values()), tuple(s.keys())),
      lambda k, xs: dict_wrapper(zip(k, xs)))

