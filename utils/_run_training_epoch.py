
def _run_training_epoch(model, optimizer, clip_ratio, value_coef, entropy_coef, device, batch_size, replay_buffer):
    from factory.tensorboard_logger import TBLogger
    tb_logger = TBLogger.get()
    model.train()
    size = len(replay_buffer)
    num_batches = max(1, size // batch_size)
    for _ in range(num_batches):
        try:
            samples, weights, indices = replay_buffer.sample_with_weights(batch_size)
        except ValueError:
            break
        b_states = torch.FloatTensor([s[0][0] for s in samples]).to(device)
        b_old_log_probs = torch.FloatTensor([s[0][1] for s in samples]).to(device)
        b_advantages = torch.FloatTensor([s[0][2] for s in samples]).to(device)
        b_actions = torch.LongTensor([s[1] for s in samples]).to(device)
        b_returns = torch.FloatTensor([s[2] for s in samples]).to(device)
        weights_t = torch.FloatTensor(weights).to(device)
        logits, b_values = model(b_states)
        b_values = b_values.squeeze(-1)
        dist = Categorical(logits=logits)
        new_log_probs = dist.log_prob(b_actions)
        ratio = torch.exp(new_log_probs - b_old_log_probs)
        surr1 = ratio * b_advantages
        surr2 = torch.clamp(ratio, 1.0 - clip_ratio, 1.0 + clip_ratio) * b_advantages
        policy_loss = -(torch.min(surr1, surr2) * weights_t).mean()
        value_loss = (nn.MSELoss(reduction='none')(b_values, b_returns) * weights_t).mean()
        entropy = dist.entropy().mean()
        loss = policy_loss + value_coef * value_loss - entropy_coef * entropy
        optimizer.zero_grad(); loss.backward()
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
        optimizer.step()
        with torch.no_grad():
            new_td_errors = (b_returns - b_values).abs().cpu().numpy()
        replay_buffer.update_priorities(indices, new_td_errors)
        tb_logger.log_scalar("ppo/batch_loss", loss.item())
        tb_logger.increment_step()
    replay_buffer.anneal_beta()

