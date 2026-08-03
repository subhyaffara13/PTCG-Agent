import itertools

def _mosaic_gpu_abstract_eval(*_, module, out_types, inout_types):
  del module # Unused.
  return [
      jax_core.ShapedArray(t.shape, t.dtype)
      for t in itertools.chain(out_types, inout_types)
  ]

