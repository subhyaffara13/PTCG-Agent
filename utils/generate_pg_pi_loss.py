
def generate_pg_pi_loss(net_apply, loss_class, entropy_cost, l2_actor_weight):
  """A function generator generates loss function."""

  def _pg_loss(net_params, batch):
    info_states = batch["info_states"]
    policy_logits, q_values = net_apply(net_params, info_states)
    chex.assert_equal_shape([policy_logits, q_values])
    pi_loss = loss_class(logits_t=policy_logits, q_t=q_values)
    ent_loss = rlax.entropy_loss(
        logits_t=policy_logits, w_t=jnp.ones(policy_logits.shape[:1]))
    l2_loss = jnp.sum(jnp.square(jax.flatten_util.ravel_pytree(net_params)[0]))
    return pi_loss + entropy_cost * ent_loss + l2_actor_weight * l2_loss

  return _pg_loss

