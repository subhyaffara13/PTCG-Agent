
def with_memory_space_constraint_abstract_eval(x, *, memory_space):
  if not isinstance(x, jax_core.ShapedArray):
    raise NotImplementedError("with_memory_space_constraint only supports "
                              "arrays.")
  return x.update(memory_space=memory_space)

