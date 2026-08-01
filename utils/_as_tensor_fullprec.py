
def _as_tensor_fullprec(t):
    """
    Like torch.as_tensor, but when given Python data types it will keep
    them in full precision.  Used for calling convention for Dynamo.
    Python scalars (float, int) are always created on CPU to avoid being
    affected by DeviceContext.
    """
    ty = type(t)
    if ty is builtins.float:
        return torch.as_tensor(t, dtype=torch.float64, device="cpu")
    elif ty is builtins.int:
        return torch.as_tensor(t, dtype=torch.int64, device="cpu")
    else:
        return torch.as_tensor(t)

