
def get_default_load_endianness() -> LoadEndianness | None:
    """
    Get fallback byte order for loading files

    If byteorder mark is not present in saved checkpoint,
    this byte order is used as fallback.
    By default, it's "native" byte order.

    Returns:
        default_load_endian: Optional[LoadEndianness]
    """
    from torch.utils.serialization import config

    return config.load.endianness

