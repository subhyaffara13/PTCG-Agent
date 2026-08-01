
def _broadcast_processed_state(
    fsdp_state: _FSDPState,
    optim_state: dict[str, Any],
    group: dist.ProcessGroup | None,
) -> dict[str, Any]:
    objects: list[Any] = [None]
    if dist.get_rank(group) == 0:
        objects[0] = tree_map_only(
            torch.Tensor,
            lambda v: v.cpu() if v.dim() == 0 else _PosDimTensorInfo(v.shape, v.dtype),  # type: ignore[union-attr]
            optim_state,
        )
    dist.broadcast_object_list(objects, src=0, group=group)
    if dist.get_rank(group) == 0:
        return optim_state
    else:
        return objects[0]

