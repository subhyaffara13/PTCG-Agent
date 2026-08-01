
def _shard_typed_scalar(xs, shardings, layouts, copy_semantics):
  return _shard_np_array(
      [literals.TypedNdArray(
        np.array(x, dtype=x.dtype),
        aval=core.ShapedArray((), x.dtype, weak_type=True))
       for x in xs],
      shardings, layouts, copy_semantics
  )

