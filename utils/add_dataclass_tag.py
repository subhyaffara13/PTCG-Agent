
def add_dataclass_tag(info: TypeInfo) -> None:
    # The value is ignored, only the existence matters.
    info.metadata["dataclass_tag"] = {}

