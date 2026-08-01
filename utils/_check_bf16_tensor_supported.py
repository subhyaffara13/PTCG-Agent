
def _check_bf16_tensor_supported(device: Device):
    try:
        torch.tensor([1.0], dtype=torch.bfloat16, device=device)
        return True
    except Exception:
        return False

