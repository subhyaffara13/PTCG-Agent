
def _prepare_training(model, device, states, actions, old_log_probs, rewards, gamma, lam):
    from factory.tensorboard_logger import TBLogger
    tb_logger = TBLogger.get()
    states_t = torch.FloatTensor(states).to(device)
    actions_t = torch.LongTensor(actions).to(device)
    old_log_probs_t = torch.FloatTensor(old_log_probs).to(device)
    rewards_t = torch.FloatTensor(rewards).to(device)
    logger.info(f"  Training on {len(states)} samples, Mean reward: {rewards_t.mean().item():.4f}")
    unique_actions = len(set(actions))
    logger.info(f"  Action diversity: {unique_actions}")
    model.eval()
    with torch.no_grad():
        _, values_t = model(states_t)
        values_t = values_t.squeeze(-1)
    advantages_t, returns_t = _compute_gae(rewards_t, values_t, device, gamma, lam)
    advantages_t = (advantages_t - advantages_t.mean()) / (advantages_t.std(unbiased=False) + 1e-8)
    td_errors = (returns_t - values_t).abs().cpu().numpy()
    from factory.replay_buffer import ReplayBuffer
    replay_buffer = ReplayBuffer(capacity=len(states), expert_ratio=0.0)
    for i in range(len(states)):
        state_payload = (states[i], old_log_probs[i], advantages_t[i].item())
        replay_buffer.add_self_play(state_payload, actions[i], returns_t[i].item(), td_error=td_errors[i])
    return states_t, actions_t, old_log_probs_t, rewards_t, advantages_t, returns_t, replay_buffer

