
def _reject_complex(params):
  if any(jnp.iscomplexobj(x) for x in jax.tree.leaves(params)):
    raise ValueError('This transformation does not support complex parameters.')

