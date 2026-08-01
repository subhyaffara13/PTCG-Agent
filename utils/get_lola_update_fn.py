
def get_lola_update_fn(
    agent_id: int,
    policy_network: hk.Transformed,
    optimizer: optax.TransformUpdateFn,
    pi_lr: float,
    gamma: float = 0.99,
    lola_weight: float = 1.0,
) -> UpdateFn:
  """Get the LOLA update function.

  Returns a function that updates the policy parameters using the LOLA
  correction formula.
  
  Args:
      agent_id: the agent's id
      policy_network: A haiku transformed policy network.
      optimizer: An optax optimizer.
      pi_lr: Policy learning rate.
      gamma: Discount factor.
      lola_weight: The LOLA correction weight to scale the correction term.

  Returns:
      A UpdateFn function that updates the policy parameters.
  """

  def flat_params(
      params,
  ) -> typing.Tuple[
      typing.Dict[str, jnp.ndarray], typing.Dict[typing.Any, typing.Callable]
  ]:
    """Flattens the policy parameters.
    
    Flattens the parameters of the policy network into a single vector and
    returns the unravel function.
    
    Args:
        params: The policy parameters.

    Returns:
        A tuple (flat_params, unravel_fn)
    """
    flat_param_dict = {
        agent_id: jax.flatten_util.ravel_pytree(p)
        for agent_id, p in params.items()
    }

    params = dict((k, flat_param_dict[k][0]) for k in flat_param_dict)
    unravel_fns = dict((k, flat_param_dict[k][1]) for k in flat_param_dict)
    return params, unravel_fns

  def lola_correction(
      train_state: TrainState, batch: TransitionBatch
  ) -> hk.Params:
    """Computes the LOLA correction term.

    Args:
        train_state: The agent's current train state.
        batch: A transition batch.

    Returns:
        The LOLA correction term.
    """
    a_t, o_t, r_t, values = (
        batch.action,
        batch.info_state,
        batch.reward,
        batch.values,
    )
    params, unravel_fns = flat_params(train_state.policy_params)

    compute_returns = partial(rlax.lambda_returns, lambda_=0.0)
    g_t = vmap(vmap(compute_returns))(
        r_t=r_t, v_t=values, discount_t=jnp.full_like(r_t, gamma)
    )
    g_t = (g_t - g_t.mean()) / (g_t.std() + 1e-8)

    def log_pi(params, i, a_t, o_t):
      return policy_network.apply(unravel_fns[i](params), o_t).log_prob(a_t)

    opp_id = 1 - agent_id

    def cross_term(a_t, o_t, r_t):
      """Computes the second order correction term of the LOLA update.

      Args:
          a_t: actions of both players
          o_t: observations of both players
          r_t: rewards of both players

      Returns:
          The second order correction term.
      """
      grad_log_pi = vmap(jax.value_and_grad(log_pi), in_axes=(None, None, 0, 0))
      log_probs, grads = grad_log_pi(
          params[agent_id], agent_id, a_t[agent_id], o_t[agent_id]
      )
      opp_logrpobs, opp_grads = grad_log_pi(
          params[opp_id], opp_id, a_t[opp_id], o_t[opp_id]
      )
      grads = grads.cumsum(axis=0)
      opp_grads = opp_grads.cumsum(axis=0)
      log_probs = log_probs.cumsum(axis=0)
      opp_logrpobs = opp_logrpobs.cumsum(axis=0)
      cross_term = 0.0
      for t in range(0, len(a_t[agent_id])):
        discounted_reward = r_t[opp_id, t] * jnp.power(gamma, t)
        cross_term += (
            discounted_reward
            * jnp.outer(grads[t], opp_grads[t])
            * jnp.exp(log_probs[t] + opp_logrpobs[t])
        )
      return cross_term  # * jnp.exp(log_probs.sum() + opp_logrpobs.sum())

    def policy_gradient(a_t, o_t, g_t):
      grad_log_pi = vmap(grad(log_pi), in_axes=(None, None, 0, 0))
      opp_grads = grad_log_pi(params[opp_id], opp_id, a_t[opp_id], o_t[opp_id])
      pg = g_t[agent_id] @ opp_grads
      return pg

    cross = vmap(cross_term, in_axes=(1, 1, 1))(a_t, o_t, r_t).mean(axis=0)
    pg = vmap(policy_gradient, in_axes=(1, 1, 1))(a_t, o_t, g_t).mean(axis=0)
    correction = -pi_lr * (pg @ cross)
    return unravel_fns[agent_id](correction)

  def policy_loss(params, agent_id, batch):
    """Computes the policy gradient loss.

    Args:
        params: The policy parameters.
        agent_id: The agent's id.
        batch: A transition batch.

    Returns:
        The policy gradient loss.
    """
    a_t, o_t, r_t, values = (
        batch.action[agent_id],
        batch.info_state[agent_id],
        batch.reward[agent_id],
        batch.values[agent_id],
    )
    logits_t = vmap(vmap(lambda s: policy_network.apply(params, s).logits))(o_t)
    discount = jnp.full(r_t.shape, gamma)
    returns = vmap(rlax.lambda_returns)(
        r_t=r_t,
        v_t=values,
        discount_t=discount,
        lambda_=jnp.ones_like(discount),
    )
    adv_t = returns - values
    loss = vmap(rlax.policy_gradient_loss)(
        logits_t=logits_t, a_t=a_t, adv_t=adv_t, w_t=jnp.ones_like(adv_t)
    )
    return loss.mean()

  def update(
      train_state: TrainState, batch: TransitionBatch
  ) -> typing.Tuple[TrainState, typing.Dict]:
    """Updates the policy parameters in train_state.

    If lola_weight > 0, the correction term by Foerster et al. will be applied.

    Args:
        train_state: the agent's train state.
        batch: a transition batch

    Returns:
        A tuple (new_train_state, metrics)
    """
    loss, policy_grads = jax.value_and_grad(policy_loss)(
        train_state.policy_params[agent_id], agent_id, batch
    )
    correction = lola_correction(train_state, batch)
    policy_grads = jax.tree_util.tree_map(
        lambda grad, corr: grad - lola_weight * corr, policy_grads, correction
    )
    updates, opt_state = optimizer(
        policy_grads, train_state.policy_opt_states[agent_id]
    )
    policy_params = optax.apply_updates(
        train_state.policy_params[agent_id], updates
    )
    train_state = TrainState(
        policy_params={**train_state.policy_params, agent_id: policy_params},
        policy_opt_states={
            **train_state.policy_opt_states,
            agent_id: opt_state,
        },
        critic_params=deepcopy(train_state.critic_params),
        critic_opt_states=deepcopy(train_state.critic_opt_states),
    )
    return train_state, {'loss': loss}

  return update

