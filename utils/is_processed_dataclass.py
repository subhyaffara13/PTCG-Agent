
def is_processed_dataclass(info: TypeInfo) -> bool:
    return bool(info) and "dataclass" in info.metadata

