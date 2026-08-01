
def _compute_old_log_probs(model, device, states):
    """Evaluate current policy log-probabilities for the given states."""
    if not hasattr(model, 'flat_base'):
        return None
    states_t = torch.FloatTensor(states).to(device)
    model.eval()
    with torch.no_grad():
        logits, _ = model(states_t)
        dist = Categorical(logits=logits)
        return dist.log_prob(torch.argmax(logits, dim=-1)).cpu().tolist()


def _compute_old_log_probs(model, device, states):
    """Evaluate current policy log-probabilities for the given states."""
    if not hasattr(model, 'flat_base'):
        return None
    states_t = torch.FloatTensor(states).to(device)
    model.eval()
    with torch.no_grad():
        logits, _ = model(states_t)
        dist = Categorical(logits=logits)
        return dist.log_prob(torch.argmax(logits, dim=-1)).cpu().tolist()

