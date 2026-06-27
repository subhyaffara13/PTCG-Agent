import time
import os
import logging
from typing import Tuple

logger = logging.getLogger(__name__)

def run_evaluation_loader(model, loader, device, criterion) -> Tuple[float, float]:
    try:
        import torch
    except ImportError:
        return 0.0, 0.0
    model.eval()
    total_loss, correct, total = 0.0, 0, 0
    with torch.no_grad():
        for states, actions in loader:
            states, actions = states.to(device), actions.to(device)
            outputs = model(states)
            total_loss += criterion(outputs, actions).item()
            _, predicted = torch.max(outputs.data, 1)
            total += actions.size(0)
            correct += (predicted == actions).sum().item()
    return total_loss / len(loader), 100 * correct / total

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
