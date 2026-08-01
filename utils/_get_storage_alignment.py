
def _get_storage_alignment() -> int:
    """
    Gets alignment for storages in torch.save files/

    Defaults to 64.

    Returns:
        storage_alginment: int
    """
    from torch.utils.serialization import config

    return config.save.storage_alignment

