
def _is_meta_location(map_location):
    """
    Check if map_location specifies the meta device.

    This is used to skip reading storage data from disk when loading
    to the meta device, since meta tensors don't hold actual data.

    Args:
        map_location: The map_location argument passed to torch.load

    Returns:
        True if map_location is definitively the meta device, False otherwise.
        For dict or callable map_location, returns False since we can't
        easily determine the target device without evaluating it.
    """
    if map_location is None:
        return False
    if isinstance(map_location, str):
        return map_location == "meta"
    if isinstance(map_location, torch.device):
        return map_location.type == "meta"
    # dict or callable - can't easily determine
    return False

