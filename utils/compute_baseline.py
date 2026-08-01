
def compute_baseline(policy, action_values):
  # V = pi * Q, backprop through pi but not Q.
  return torch.sum(torch.mul(policy, action_values.detach()), dim=1)

