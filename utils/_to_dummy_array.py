
def _to_dummy_array(x):
  if isinstance(x,jax.ShapeDtypeStruct):
    return ArrayRepr(x.shape, x.dtype)
  elif isinstance(x, jax.Array | np.ndarray):
    return ArrayRepr.from_array(x)
  elif graphlib.is_graph_node(x):
    return SimpleObjectRepr(x)
  else:
    return x

