
def log_binom(n, k, eps=1e-7):
    """log(nCk) using stirling approximation"""
    n = n + eps
    k = k + eps
    return n * torch.log(n) - k * torch.log(k) - (n - k) * torch.log(n - k + eps)

