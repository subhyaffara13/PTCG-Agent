
def _commute_transform(
    aval: jax_core.AbstractValue,
    t1: state_types.Transform,
    t2: state_types.Transform,
) -> tuple[state_types.Transform, state_types.Transform]:
  """Commutes two transforms.

  We pass in an `aval` to handle cases where the transforms, by themselves, do
  not provide enough information to determine how to commute.

  Args:
    aval: An abstract value.
    t1: A transform.
    t2: Another transform.

  Returns:
    Returns a tuple of transforms (t2', t1') such that
    t2'(t1'(aval)) == t1(t2(aval)).
  """
  match t1, t2:
    case (
        (
            gpu_core.UntilingTransform()
            | gpu_core.UnswizzleRef()
            | gpu_core.ExpandLeadingBatchDimensionsTransform()
        ) as t1,
        indexing.NDIndexer() as t2,
    ):
      new_indexer, new_t1 = t1.commute_ndindexer(aval, t2)
      return new_indexer, new_t1
    case (
        state_types.TransposeTransform() as t1,
        indexing.NDIndexer() as t2,
    ):
      return gpu_core.commute_transpose_indexer(aval, t1, t2)
    case (
        gpu_core.UnswizzleRef() as t1,
        state_types.ReshapeTransform() as t2,
    ):
      # pyrefly: ignore[bad-argument-type]
      new_reshape, new_unswizzle = t1.commute_reshape(aval, t2)
      return new_reshape, new_unswizzle
    case (
        gpu_core.UntilingTransform() | gpu_core.UnswizzleRef() as t1,
        gpu_core.TransposeTransform() as t2,
    ):
      if isinstance(aval, state_types.AbstractRef):
        aval = aval.inner_aval
      assert isinstance(aval, jax_core.ShapedArray)
      new_reshape, new_unswizzle = t1.commute_transpose(aval, t2)
      return new_reshape, new_unswizzle
    case (
        gpu_core.UntilingTransform() as t1,
        state_types.ReshapeTransform() as t2,
    ):
      if isinstance(aval, state_types.AbstractRef):
        aval = aval.inner_aval
      assert isinstance(aval, jax_core.ShapedArray)
      new_reshape, new_untile = t1.commute_reshape(aval, t2)
      return new_reshape, new_untile
    case (
        gpu_core.UntilingTransform() | gpu_core.UnswizzleRef() as t1,
        gpu_core.ClusterRefTransform()
        | gpu_core.MulticastRef()
        | gpu_core.PeerMemRef() as t2,
    ):
      return t2, t1
    case _:
      raise NotImplementedError(t1, t2)

