
def learn(
    history,
    optimizer_actor,
    optimize_critic,
    agent,
    num_minibatches=5,
    update_epochs=5,
    itr_eps=0.05,
    eps_eps=0.2,
    alpha=0.5,
    ent_coef=0.01,
    max_grad_norm=5,
):
  """Update the agent network (actor and critic)."""
  v_loss = None
  batch_size = history["actions"].shape[0]
  b_inds = np.arange(batch_size)
  mini_batch_size = batch_size // num_minibatches
  # get batch indices
  np.random.shuffle(b_inds)
  for _ in range(update_epochs):
    for start in range(0, batch_size, mini_batch_size):
      end = start + mini_batch_size
      mb_inds = b_inds[start:end]
      # for each update epoch shuffle the batch indices
      # generate the new logprobs, entropy and value then calculate the ratio
      b_obs = history["info_state"][mb_inds]
      b_advantages = history["advantages"][mb_inds]

      # Get the data under the episode policy (representative agent current
      # policy)
      _, newlogprob, entropy, new_value = agent.get_action_and_value(
          b_obs, history["actions"][mb_inds]
      )
      logratio = newlogprob - history["logprobs"][mb_inds]
      ratio = torch.exp(logratio)

      # Get the data under the iteration policy (the population policy)
      _, t_newlogprob, _, _ = agent.get_action_and_value(
          b_obs, history["t_actions"][mb_inds]
      )
      t_logratio = t_newlogprob - history["t_logprobs"][mb_inds]
      t_ratio = torch.exp(t_logratio)

      # iteration update PPO
      t_pg_loss1 = b_advantages * t_ratio
      t_pg_loss2 = b_advantages * torch.clamp(t_ratio, 1 - itr_eps, 1 + itr_eps)

      # episodic update PPO
      pg_loss1 = b_advantages * ratio
      pg_loss2 = b_advantages * torch.clamp(ratio, 1 - eps_eps, 1 + eps_eps)

      # Calculate the loss using our loss function
      pg_loss = (
          -alpha * torch.min(pg_loss1, pg_loss2).mean()
          - (1 - alpha) * torch.min(t_pg_loss1, t_pg_loss2).mean()
      )
      v_loss = F.smooth_l1_loss(
          new_value.reshape(-1), history["returns"][mb_inds]
      ).mean()
      entropy_loss = entropy.mean()
      loss = pg_loss - ent_coef * entropy_loss

      # Actor update
      optimizer_actor.zero_grad()
      loss.backward()
      nn.utils.clip_grad_norm_(agent.actor.parameters(), max_grad_norm)
      optimizer_actor.step()

      # Critic update
      optimize_critic.zero_grad()
      v_loss.backward()
      nn.utils.clip_grad_norm_(agent.critic.parameters(), max_grad_norm)
      optimize_critic.step()

  assert v_loss is not None
  return v_loss

