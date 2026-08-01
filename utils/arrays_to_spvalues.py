
def arrays_to_spvalues(
    spenv: SparsifyEnv,
    args: Any
    ) -> Any:
  """Convert a pytree of (sparse) arrays to an equivalent pytree of spvalues."""
  def array_to_spvalue(arg):
    if isinstance(arg, BCOO):
      return spenv.sparse(arg.shape, arg.data, arg.indices,
                          indices_sorted=arg.indices_sorted,
                          unique_indices=arg.unique_indices)
    elif isinstance(arg, BCSR):
      return spenv.sparse(arg.shape, arg.data, arg.indices, arg.indptr,
                          indices_sorted=arg.indices_sorted,
                          unique_indices=arg.unique_indices)
    else:
      return spenv.dense(arg)
  return tree_map(array_to_spvalue, args, is_leaf=_is_sparse_obj)

