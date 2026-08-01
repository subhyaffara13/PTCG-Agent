
def _prepare_pytorch(x: torch.Tensor) -> np.ndarray:
    if x.dtype == torch.bfloat16:
        x = x.to(torch.float16)
    # pyrefly: ignore [bad-assignment]
    x = x.detach().cpu().numpy()
    # pyrefly: ignore [bad-return]
    return x

