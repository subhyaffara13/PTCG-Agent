
def lower_with_transformed_refs(f, args, avals, block_shapes=None):
  """Lower f with args as potentially nested TransformedRefs."""
  # If block_shapes is not provided, infer them from the avals.
  if block_shapes is None:
    aval_leaves, tree = tpu_primitives._dma_flatten(avals)
    aval_shapes = jax.tree.map(lambda x: x.shape, aval_leaves)
    (block_shapes,) = _dma_unflatten(tree, aval_shapes)
  args = list(zip(args, avals, block_shapes))
  return _lower_transformed_refs(f, [], args)

