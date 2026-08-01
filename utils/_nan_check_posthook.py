
def _nan_check_posthook(fun, args, kwargs, output):
  """Hook function called by the C++ jit/pmap to perform NaN checking."""
  buffers = []
  for leaf in tree_leaves(output):
    if hasattr(leaf, "addressable_shards"):
      buffers.extend([shard.data for shard in leaf.addressable_shards])

  try:
    dispatch.check_special(pjit.jit_p.name, buffers)
  except api_util.InternalFloatingPointError as e:
    assert config.debug_nans.value or config.debug_infs.value
    if hasattr(fun, '_fun'):
      f = fun._fun
      if getattr(f, '_apply_primitive', False):
        raise FloatingPointError(f"invalid value ({e.ty}) encountered in {f.__qualname__}") from None
      # compiled_fun can only raise in this case
      api_util.maybe_recursive_nan_check(e, f, args, kwargs)
      raise AssertionError("Unreachable") from e
    else:
      # TODO(emilyaf): Shouldn't need this fallback.
      raise

