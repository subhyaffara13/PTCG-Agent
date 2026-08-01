
def _get_batching_dim_factor_name(batch_group: str,batch_dim_order : int):
  """Constructs a factor name for a batching dimension.

  We expand the leading ... into factors representing the batching dimensions
  to support building the MLIR representation for the sharding rule. For this
  reason, we construct a factor name that won't be used by users for the
  batching dimensions.
  """
  return f"{_BATCHING_DIM_FACTOR_PREFIX}{batch_group}_{batch_dim_order}"

