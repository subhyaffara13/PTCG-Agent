
def _compute_gae(rewards, values, device, gamma=0.99, lam=0.95):
    advantages = torch.zeros_like(rewards)
    last_adv = 0
    padded_values = torch.cat([values, torch.tensor([0.0]).to(device)])
    for t in reversed(range(len(rewards))):
        delta = rewards[t] + gamma * padded_values[t + 1] - padded_values[t]
        advantages[t] = last_adv = delta + gamma * lam * last_adv
    return advantages, advantages + values


def _compute_gae(rewards, values, device, gamma=0.99, lam=0.95):
    advantages = torch.zeros_like(rewards)
    last_adv = 0
    padded_values = torch.cat([values, torch.tensor([0.0]).to(device)])
    for t in reversed(range(len(rewards))):
        delta = rewards[t] + gamma * padded_values[t + 1] - padded_values[t]
        advantages[t] = last_adv = delta + gamma * lam * last_adv
    return advantages, advantages + values

