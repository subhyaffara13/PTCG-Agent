
def generate_act_func(net_apply):
  """A function generator generates act function."""

  def _act(net_params, info_state, action_mask, rng):
    info_state = jnp.reshape(info_state, [1, -1])
    policy_logits, _ = net_apply(net_params, info_state)
    policy_probs = jax.nn.softmax(policy_logits, axis=1)

    # Remove illegal actions, re-normalize probs
    probs = policy_probs[0] * action_mask

    probs /= jnp.sum(probs)
    action = jax.random.choice(rng, len(probs), p=probs)
    return action, probs

  return _act

