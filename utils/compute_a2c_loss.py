
def compute_a2c_loss(policy_logits, actions, advantages):
  cross_entropy = F.cross_entropy(policy_logits, actions, reduction="none")
  advantages = advantages.detach()
  if advantages.ndim != cross_entropy.ndim:
    raise ValueError("Shapes %s and %s are not compatible" %
                     (advantages.ndim, cross_entropy.ndim))
  return torch.mul(cross_entropy, advantages)

