
def _split_layout_and_sharding(entries):
  entries_flat, treedef = tree_flatten(entries, is_leaf=lambda x: x is None)
  layouts, shardings = [], []

  for e in entries_flat:
    if isinstance(e, Format):
      layouts.append(e.layout)
      shardings.append(e.sharding)
    elif isinstance(e, (Layout, AutoLayoutSingleton)):
      raise ValueError(
          '`jax.jit` does not accept device-local layouts directly. Create '
          'a `Format` instance wrapping this device-local layout and pass '
          f'that to `jit` instead. Got {e}')
    else:
      layouts.append(None)
      shardings.append(e)

  assert len(layouts) == len(shardings)
  return tree_unflatten(treedef, layouts), tree_unflatten(treedef, shardings)

