
def get_crc32_options() -> bool:
    """
    Get whether :func:`torch.save` computes and writes crc32 for each record.

    Defaults to ``True``.
    """
    from torch.utils.serialization import config

    return config.save.compute_crc32

