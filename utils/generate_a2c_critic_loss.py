
def generate_a2c_critic_loss(net_apply, l2_critic_weight, lambda_):
  """A function generator generates loss function."""

  def _a2c_critic_loss(net_params, batch):
    info_states, rewards, discounts = batch["info_states"], batch[
        "rewards"], batch["discounts"]
    _, baselines = net_apply(net_params, info_states)
    baselines = jnp.squeeze(baselines, axis=1)
    baselines = jnp.concatenate([baselines[:-1], jnp.zeros(1)])

    td_lambda = rlax.td_lambda(
        v_tm1=baselines[:-1],
        r_t=rewards,
        discount_t=discounts,
        v_t=baselines[1:],
        lambda_=lambda_,
        stop_target_gradients=True)
    l2_loss = jnp.sum(jnp.square(jax.flatten_util.ravel_pytree(net_params)[0]))
    return jnp.mean(jnp.square(td_lambda)) + l2_critic_weight * l2_loss

  return _a2c_critic_loss

