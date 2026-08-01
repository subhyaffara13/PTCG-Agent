
def thresholded(
    logits: torch.Tensor, regrets: torch.Tensor, threshold: float = 2.0
) -> torch.Tensor:
  """Zeros out `regrets` where `logits` are too negative or too large."""
  can_decrease = torch.gt(logits, -threshold).float()
  can_increase = torch.lt(logits, threshold).float()
  regrets_negative = -F.relu(-regrets)
  regrets_positive = F.relu(regrets)
  return can_decrease * regrets_negative + can_increase * regrets_positive


def thresholded(logits, regrets, threshold=2.0):
  """Zeros out `regrets` where `logits` are too negative or too large."""
  can_decrease = logits.gt(-threshold).float()
  can_increase = logits.lt(threshold).float()
  regrets_negative = regrets.clamp(max=0.0)
  regrets_positive = regrets.clamp(min=0.0)
  return can_decrease * regrets_negative + can_increase * regrets_positive

