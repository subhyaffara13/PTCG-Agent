
def compute_entropy(policy_logits):
  return torch.sum(
      -F.softmax(policy_logits, dim=1) * F.log_softmax(policy_logits, dim=1),
      dim=-1)

