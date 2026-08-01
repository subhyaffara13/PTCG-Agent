
def simple_make_perturbed_fun(f, num_samples=1000, sigma=0.1,
                              noise=_make_pert.Gumbel()):
  # a simplified Monte Carlo estimate of E[f(x + σ Z)] where Z ~ noise
  # this simplified reference only works for differentiable f
  @jax.jit
  def g(key, x):
    zs_shape = optax.tree.batch_shape(x, (num_samples,))
    zs = optax.tree.random_like(key, zs_shape, noise.sample)
    xs = optax.tree.add_scale(x, sigma, zs)
    ys = jax.vmap(f)(xs)
    ys_mean = jax.tree.map(lambda leaf: jnp.mean(leaf, 0), ys)
    return ys_mean
  return g

