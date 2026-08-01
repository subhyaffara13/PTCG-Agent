
def sample_group_sizes(key: jax.Array,
                       num_groups: int,
                       num_elements: int,
                       alpha: float = 10.0,
                       ):
  """Sample group sizes.

  Args:
    key: PRNG key.
    num_groups: Number of groups to sample.
    num_elements: Total number of elements to sample.
    alpha: Shape parameter. The lower the alpha, the more imbalanced the
      group sizes will be. As alpha approaches infinity, the group sizes
      approach a uniform distribution.

  Returns:
    A jax.Array of shape (num_groups,) that sums to num_elements.
  """
  probs_key, sample_key = jax.random.split(key)
  probs = jax.random.dirichlet(probs_key, jnp.ones((num_groups,)) * alpha)
  return jax.random.multinomial(
      sample_key, num_elements, probs).astype(jnp.int32)

