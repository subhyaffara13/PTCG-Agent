from typing import Tuple

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

