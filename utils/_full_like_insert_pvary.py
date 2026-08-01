
def _full_like_insert_pvary(val, x):
  if not config.auto_pcast.value:
    return val
  from jax._src.state.types import TransformedRef  # pyrefly: ignore[missing-import]
  if isinstance(x, TransformedRef):
    all_varying = frozenset.union(*[
        typeof(l).mat.varying for l in tree_util.FlatTree.flatten(x).vals
    ])
    return core.pvary(val, all_varying)
  else:
    val, _ = core.auto_insert_reshard(val, x)
    return val

