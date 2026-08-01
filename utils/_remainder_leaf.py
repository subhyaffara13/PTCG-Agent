
def _remainder_leaf(leaf, batch_elems):
  def f(l):
    return l[batch_elems:]
  sharding = canonicalize_sharding(core.typeof(leaf).sharding, 'lax.map')
  if sharding is not None and sharding.mesh._any_axis_explicit:
    return auto_axes(
        f, out_sharding=sharding, axes=sharding.mesh.explicit_axes
    )(leaf)
  return f(leaf)

