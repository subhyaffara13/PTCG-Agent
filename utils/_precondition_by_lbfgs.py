
def _precondition_by_lbfgs(
    updates: base.Updates,
    diff_params_memory: base.ArrayTree,
    diff_updates_memory: base.ArrayTree,
    weights_memory: jax.typing.ArrayLike,
    identity_scale: jax.typing.ArrayLike,  # float
    memory_idx: jax.typing.ArrayLike,  # int
) -> base.Updates:
  r"""Multiplies updates by an approximation of the inverse Hessian.

  The approximation of the inverse Hessian is parameterized
  by rank one matrices defined by past differences of parameters and
  gradients/updates. See :func:`optax.scale_by_lbfgs` for the mathematical
  formulation.

  Args:
    updates: updates (gradients a priori) to be multiplied by approximate
      inverse Hessian.
    diff_params_memory: represents a list of past parameters' differences.
    diff_updates_memory: represents a list of past gradients/updates'
      differences.
    weights_memory: list of past weights multiplying the rank one matrices
      defining the inverse Hessian approximation, see
      :func:`optax.scale_by_lbfgs` for more details.
    identity_scale: scaling factor multiplying an identity matrix used as an
      initial approximation of the inverse Hessian (:math:`\gamma` in the
      formulation given in :func:`optax.scale_by_lbfgs`).
    memory_idx: current index between ``0`` and ``memory_size-1`` in the memory
      buffer.

  Returns:
    Preconditioned updates, that is, updates multiplied by an approximation of
    the inverse Hessian defined by past parameters and gradients/updates
    differences up to some predetermined memory buffer size.

  Reference:
    Algorithm 7.4 (page 178) in Nocedal et al, `Numerical Optimization
    <https://www.math.uci.edu/~qnie/Publications/NumericalOptimization.pdf>_`
    , 1999
  """
  rhos = weights_memory
  memory_size = weights_memory.shape[0]  # pytype: disable=attribute-error  # jax-arraylike # noqa: E501
  indices = (memory_idx + jnp.arange(memory_size)) % memory_size

  def right_product(vec, idx):
    dwi, dui = jax.tree.map(
        lambda x: x[idx], (diff_params_memory, diff_updates_memory)
    )
    alpha = rhos[idx] * optax.tree.real(optax.tree.vdot(dwi, vec))
    vec_new = optax.tree.add_scale(vec, -alpha, dui)
    vec_new = optax.tree.cast_like(vec_new, vec)
    return vec_new, alpha

  precond_updates, alphas = jax.lax.scan(
      right_product, updates, indices, reverse=True
  )

  precond_updates = optax.tree.scale(identity_scale, precond_updates)

  def left_product(vec, idx_alpha):
    idx, alpha = idx_alpha
    dwi, dui = jax.tree.map(
        lambda x: x[idx], (diff_params_memory, diff_updates_memory)
    )
    beta = rhos[idx] * optax.tree.real(optax.tree.vdot(dui, vec))
    vec_new = optax.tree.add_scale(vec, alpha - beta, dwi)
    vec_new = optax.tree.cast_like(vec_new, vec)
    return vec_new, beta

  precond_updates, _ = jax.lax.scan(
      left_product, precond_updates, (indices, alphas)
  )

  return precond_updates

