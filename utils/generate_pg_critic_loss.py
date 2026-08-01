
def generate_pg_critic_loss(net_apply, l2_critic_weight, lambda_):
  """A function generator generates loss function."""

  def _critic_loss(net_params, batch):
    info_states, actions, rewards, discounts = batch["info_states"], batch[
        "actions"], batch["rewards"], batch["discounts"]
    _, q_values = net_apply(net_params, info_states)
    q_values = q_values[:-1]
    q_values = jnp.concatenate(
        [q_values, jnp.zeros(q_values[-1].reshape(1, -1).shape)])

    actions = jnp.concatenate([actions, jnp.zeros(1, dtype=int)])
    sarsa_lambda = rlax.sarsa_lambda(
        q_tm1=q_values[:-1],
        a_tm1=actions[:-1],
        r_t=rewards,
        discount_t=discounts,
        q_t=q_values[1:],
        a_t=actions[1:],
        lambda_=lambda_,
        stop_target_gradients=True)
    l2_loss = jnp.sum(jnp.square(jax.flatten_util.ravel_pytree(net_params)[0]))
    return jnp.mean(jnp.square(sarsa_lambda)) + l2_critic_weight * l2_loss

  return _critic_loss

