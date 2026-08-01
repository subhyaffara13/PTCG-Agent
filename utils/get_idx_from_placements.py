
def get_idx_from_placements(placements, current_rank) -> int:
    """
    Return the position of the current rank in the given placements.

    Args:
        placements(List[Union[_remote_device, str]]):
            Specifies the placement of each shard of the Tensor. The size of
            the list represents the number of shards to be created. This could
            be a list of
            :class:`torch.distributed._remote_device`'s. This list
            could also contain a string which represents remote
            device as accepted by
            :class:`torch.distributed._remote_device`
        current_rank (int): number of current device.

    Returns:
        A int which contains the position of current device in the placement list.
    """
    for idx, placement in enumerate(placements):  # type: ignore[attr-defined]
        if current_rank == placement.rank():  # type: ignore[union-attr]
            return idx
    raise RuntimeError("current_rank not in the placement.")

