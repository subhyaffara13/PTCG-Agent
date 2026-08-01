
def _detach_traced_inputs(flat_args: Any) -> Any:
    if detect_fake_mode():
        detach_tensor = _detach_and_copy_item_memo
    else:

        def detach_tensor(t: torch.Tensor) -> torch.Tensor:
            return t.detach()

    return pytree.tree_map_only(torch.Tensor, detach_tensor, flat_args)

