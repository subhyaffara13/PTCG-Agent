
def _scan_leaf(leaf, batch_elems, num_batches, batch_size):
  def f(l):
    return l[:batch_elems].reshape(num_batches, batch_size, *leaf.shape[1:])

  aval = core.typeof(leaf)
  if aval.sharding.spec[0] is not None:
    raise ValueError(
        '0th dimension of leaf passed to `jax.lax.map` should be replicated.'
        f' Got {aval.str_short(True, True)}')

  out_s = aval.sharding.update(spec=P(None, None, *aval.sharding.spec[1:]))
  out_s = canonicalize_sharding(out_s, 'lax.map')
  if out_s is not None and out_s.mesh._any_axis_explicit:
    return auto_axes(f, out_sharding=out_s, axes=out_s.mesh.explicit_axes)(leaf)
  return f(leaf)

