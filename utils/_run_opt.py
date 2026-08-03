from typing import Callable

def _run_opt(
    opt: base.GradientTransformationExtraArgs,
    fun: Callable[[base.ArrayTree], jnp.ndarray],
    init_params: base.ArrayTree,
    maxiter: int = 500,
    tol: float = 1e-3,
) -> tuple[base.ArrayTree, base.OptState]:
  """Run LBFGS solver by iterative calls to grad transform and apply_updates."""
  value_and_grad_fun = jax.value_and_grad(fun)

  def stopping_criterion(carry):
    _, _, count, grad = carry
    return (optax.tree.norm(grad) >= tol) & (count < maxiter)

  def step(carry):
    params, state, count, _ = carry
    value, grad = value_and_grad_fun(params)
    grad = optax.tree.conj(grad)
    updates, state = opt.update(
        grad, state, params, value=value, grad=grad, value_fn=fun
    )
    params = update.apply_updates(params, updates)
    return params, state, count + 1, grad

  init_state = opt.init(init_params)
  init_grad = jax.grad(fun)(init_params)
  final_params, final_state, *_ = jax.lax.while_loop(
      stopping_criterion, step, (init_params, init_state, 0, init_grad)
  )

  return final_params, final_state

