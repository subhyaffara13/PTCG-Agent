
def _clean_dynamic_markers(tensor: torch.Tensor) -> None:
    for attr in [
        "_dynamo_weak_dynamic_indices",
        "_dynamo_dynamic_indices",
        "_dynamo_dynamic_range",
        "_dynamo_static_indices",
        "_dynamo_unbacked_indices",
    ]:
        if hasattr(tensor, attr):
            delattr(tensor, attr)

