
def _pytree_deque_flatten(xs: PytreeDeque, *, with_path: bool):
  if with_path:
    nodes = tuple((jtu.SequenceKey(i), x) for i, x in enumerate(xs))
    return nodes, ()
  else:
    return xs, ()

