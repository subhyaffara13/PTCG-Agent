
def slow_add(x, y, device="cpu"):
    time.sleep(1)
    x = x.to(device)
    y = y.to(device)
    return torch.add(x, y).cpu()

