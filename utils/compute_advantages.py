
def compute_advantages(policy_logits,
                       action_values,
                       use_relu=False,
                       threshold_fn=None):
  """Compute advantages using pi and Q."""
  # Compute advantage.
  policy = F.softmax(policy_logits, dim=1)
  # Avoid computing gradients for action_values.
  action_values = action_values.detach()

  baseline = compute_baseline(policy, action_values)

  advantages = action_values - torch.unsqueeze(baseline, 1)
  if use_relu:
    advantages = F.relu(advantages)

  if threshold_fn:
    # Compute thresholded advanteges weighted by policy logits for NeuRD.
    policy_logits = policy_logits - policy_logits.mean(-1, keepdim=True)
    advantages = threshold_fn(policy_logits, advantages)
    policy_advantages = -torch.mul(policy_logits, advantages.detach())
  else:
    # Compute advantage weighted by policy.
    policy_advantages = -torch.mul(policy, advantages.detach())
  return torch.sum(policy_advantages, dim=1)

