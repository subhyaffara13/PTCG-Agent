
def _add_empty_metadata(info: TypeInfo) -> None:
    """Add empty metadata to mark that we've finished processing this class."""
    info.metadata["attrs"] = {"attributes": [], "frozen": False}

