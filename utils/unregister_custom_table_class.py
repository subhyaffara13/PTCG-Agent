
def unregisterCustomTableClass(tag: str | bytes) -> None:
    """Unregister the custom packer/unpacker class for a table."""
    del _customTableRegistry[tag]

