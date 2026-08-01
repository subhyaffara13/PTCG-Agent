
def rollout(env, iter_agent, eps_agent, num_epsiodes, steps, device):
  """Generates num_epsiodes rollouts."""
  info_state = torch.zeros((steps, iter_agent.info_state_size), device=device)
  actions = torch.zeros((steps,), device=device)
  logprobs = torch.zeros((steps,), device=device)
  rewards = torch.zeros((steps,), device=device)
  dones = torch.zeros((steps,), device=device)
  values = torch.zeros((steps,), device=device)
  entropies = torch.zeros((steps,), device=device)
  t_actions = torch.zeros((steps,), device=device)
  t_logprobs = torch.zeros((steps,), device=device)

  step = 0
  for _ in range(num_epsiodes):
    time_step = env.reset()
    while not time_step.last():
      obs = time_step.observations["info_state"][0]
      obs = torch.Tensor(obs).to(device)
      info_state[step] = obs
      with torch.no_grad():
        t_action, t_logprob, _, _ = iter_agent.get_action_and_value(obs)
        action, logprob, entropy, ivalue = eps_agent.get_action_and_value(obs)

      time_step = env.step([action.item()])

      # iteration policy data
      t_logprobs[step] = t_logprob
      t_actions[step] = t_action

      # episode policy data
      logprobs[step] = logprob
      dones[step] = time_step.last()
      entropies[step] = entropy
      values[step] = ivalue
      actions[step] = action
      rewards[step] = torch.Tensor(time_step.rewards).to(device)
      step += 1

  history = {
      "info_state": info_state,
      "actions": actions,
      "logprobs": logprobs,
      "rewards": rewards,
      "dones": dones,
      "values": values,
      "entropies": entropies,
      "t_actions": t_actions,
      "t_logprobs": t_logprobs,
  }
  return history

