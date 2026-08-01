
def generate_a2c_pi_loss(net_apply, loss_class, entropy_cost, l2_actor_weight,
                         lambda_):
  """A function generator generates loss function."""

  def _a2c_pi_loss(net_params, batch):
    info_states, actions, rewards, discounts = batch["info_states"], batch[
        "actions"], batch["rewards"], batch["discounts"]
    policy_logits, baselines = net_apply(net_params, info_states)
    policy_logits = policy_logits[:-1]

    baselines = jnp.squeeze(baselines, axis=1)
    baselines = jnp.concatenate([baselines[:-1], jnp.zeros(1)])
    td_returns = rlax.lambda_returns(
        rewards,
        discounts,
        baselines[1:],
        lambda_=lambda_,
        stop_target_gradients=True)
    advantages = td_returns - baselines[:-1]
    chex.assert_equal_shape([td_returns, actions, advantages])
    pi_loss = loss_class(
        logits_t=policy_logits,
        a_t=actions,
        adv_t=advantages,
        w_t=jnp.ones(td_returns.shape))
    ent_loss = rlax.entropy_loss(
        logits_t=policy_logits, w_t=jnp.ones(td_returns.shape))
    l2_loss = jnp.sum(jnp.square(jax.flatten_util.ravel_pytree(net_params)[0]))
    return pi_loss + entropy_cost * ent_loss + l2_actor_weight * l2_loss

  return _a2c_pi_loss

