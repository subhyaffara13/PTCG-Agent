
def _shard_python_scalar(xs, shardings, layouts, copy_semantics):
  return shard_args(shardings, layouts, copy_semantics,
                    [np.array(x) for x in xs])

