
def _detach_and_copy_item_memo(t: torch.Tensor) -> torch.Tensor:
    detached_t = t.detach()
    if hasattr(t, "item_memo"):
        # pyrefly: ignore[missing-attribute]
        detached_t.item_memo = t.item_memo
    return detached_t

