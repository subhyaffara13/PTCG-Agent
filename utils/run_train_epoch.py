
def run_train_epoch(model, loader, device, optimizer, criterion) -> float:
    model.train()
    total_loss = 0.0
    for batch_states, batch_actions in loader:
        batch_states, batch_actions = batch_states.to(device), batch_actions.to(device)
        optimizer.zero_grad()
        loss = criterion(model(batch_states), batch_actions)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss

