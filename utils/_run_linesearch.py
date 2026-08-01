
def _run_linesearch(
    opt: base.GradientTransformationExtraArgs,
    fn: Callable[..., jax.typing.ArrayLike],
    params: base.Params,
    updates: base.Updates,
    stepsize_guess: Optional[jax.typing.ArrayLike] = None,
) -> tuple[base.Params, base.OptState]:
  """Runs the linesearch, i.e., a single update of scale_by_zoom_linesearch."""
  init_state = opt.init(params)
  if stepsize_guess is not None:
    init_state = optax.tree.set(init_state, learning_rate=stepsize_guess)

  value, grad = jax.value_and_grad(fn)(params)
  updates, final_state = opt.update(
      updates,
      init_state,
      params,
      value=value,
      grad=grad,
      value_fn=fn,
  )
  final_params = update.apply_updates(params, updates)
  return final_params, final_state

