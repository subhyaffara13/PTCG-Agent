
def checkpoint_name(x, name):
  """Identifies a value with a name within :func:`jax.checkpoint`.

  This function acts as an identity function at runtime (returning ``x``
  unchanged) but attaches a string name to the value in the JAX trace.
  These names can be targeted by specific checkpointing policies (see
  :ref:`checkpoint-policies`) to control which intermediate values
  are saved during the forward pass and which are recomputed during the
  backward pass.

  Args:
    x: array or PyTree of arrays to be named.
    name: A string name to associate with the value ``x``.

  Returns:
    The input ``x``, unchanged.

  See Also:
    - :func:`jax.checkpoint` (alias: :func:`jax.remat`): decorator to
      enable checkpointing.
    - :mod:`jax.checkpoint_policies`: a namespace containing policies
      that use names marked via ``checkpoint_name`` to determine behavior.

  Example:
    >>> import jax
    >>> import jax.numpy as jnp
    >>> from jax.ad_checkpoint import checkpoint_name

    >>> # Define a function where we explicitly name an intermediate value
    >>> def f(x):
    ...   y = jnp.sin(x)
    ...   z = checkpoint_name(y, "my_intermediate")
    ...   return jnp.cos(z)

    >>> # Use a policy that saves only the named value
    >>> policy = jax.checkpoint_policies.save_only_these_names("my_intermediate")
    >>> f_checkpointed = jax.checkpoint(f, policy=policy)

    For further examples, see the `remat example notebook
    <https://docs.jax.dev/en/latest/notebooks/autodiff_remat.html>`_.
  """
  if config.remat3.value:
    return tree_map(lambda x: checkpoint_name3(name, x), x)
  return tree_map(partial(name_p.bind, name=name), x)

