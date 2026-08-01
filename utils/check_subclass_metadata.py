
def check_subclass_metadata(value: Any, metadata: tuple[Any, ...]) -> bool:
    saved_metadata, cls, has_custom_guard = metadata
    if has_custom_guard:
        return cls.__metadata_guard__(saved_metadata, value.__tensor_flatten__()[1])
    return value.__tensor_flatten__()[1] == saved_metadata

