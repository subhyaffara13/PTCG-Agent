
def snapshot() -> dict[str, Any]:
    r"""Return a dictionary of MTIA memory allocator history"""

    return torch._C._mtia_memorySnapshot()


def snapshot(
    measure_name: str, measure: Callable[[base.Updates], base.ArrayTree]
) -> base.GradientTransformation:
  """Takes a snapshot of updates and stores it in the state.

  Useful to debug intermediate updates values in a chained transformation.

  Args:
    measure_name: Name of the measurement to store. Can be then used to retrieve
      the snapshot using `optax.tree.get(state, measure_name)`.
    measure: User callable taking as inputs updates and returning desired
      measurement. When this transformation is part of a chain, the updates are
      the transformed gradients up to that transform.

  Returns:
    A gradient transformation that captures measurements defined by the user in
    the callable `measure` and stores them in the state with the name
    `measure_name`.

  Examples:
    >>> import optax
    >>> import jax.numpy as jnp
    >>> def f(x): return jnp.sum(x ** 2)
    >>> solver = optax.chain(
    ...     optax.sgd(learning_rate=0.1, momentum=0.9),
    ...     optax.snapshot('norm_before_clip', lambda x: optax.tree.norm(x)),
    ...     optax.clip_by_global_norm(0.05)
    ... )
    >>> params = jnp.array([1., 2., 3.])
    >>> state = solver.init(params)
    >>> for step in range(2):
    ...   grads = jax.grad(f)(params)
    ...   updates, state = solver.update(grads, state)
    ...   params = optax.apply_updates(params, updates)
    ...   norm = optax.tree.get(state, 'norm_before_clip')
    ...   print(f'{step=}, {norm=:.2e}')
    step=0, norm=7.48e-01
    step=1, norm=1.41e+00

  .. versionadded: 0.2.6
  """

  def init(params: base.Params) -> SnapshotState:
    return SnapshotState({measure_name: measure(params)})

  def update(
      updates: base.Updates,
      state: SnapshotState,
      params: base.Params | None = None,
  ) -> tuple[base.Updates, SnapshotState]:
    del params, state
    return updates, SnapshotState({measure_name: measure(updates)})

  return base.GradientTransformation(init, update)

