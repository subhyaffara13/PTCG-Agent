
def _match_regret(net, obs, mask_np):
  """Returns the policy after applying regret matching."""
  with torch.no_grad():
    x = torch.from_numpy(obs).to(torch.float32)
    regrets = net(x)
    raw_regrets = regrets.cpu().numpy()

  regrets = np.clip(raw_regrets, a_min=0, a_max=None)
  regrets = regrets * mask_np
  summed = np.sum(regrets)
  if summed > 1e-6:
    return regrets / summed

  # Just use the best regret, if regrets cannot be normalized.
  max_id, max_regret = -1, float("-inf")
  for i, m in enumerate(mask_np):
    if m == 1 and raw_regrets[i] > max_regret:
      max_id, max_regret = i, raw_regrets[i]
  policy = np.zeros(regrets.shape, dtype=regrets.dtype)
  policy[max_id] = 1
  return policy

