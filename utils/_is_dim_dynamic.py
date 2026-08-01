
def _is_dim_dynamic(t: torch.Tensor, d: int) -> bool:
    return hasattr(t, "_dynamo_dynamic_indices") and d in t._dynamo_dynamic_indices

