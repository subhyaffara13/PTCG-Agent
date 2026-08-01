
def extract_subclass_metadata(guard: Any, value: Any) -> tuple[Any, ...]:
    metadata = deepcopy(value.__tensor_flatten__()[1])
    cls = type(value)
    has_custom_guard = hasattr(value, "__metadata_guard__")
    return (metadata, cls, has_custom_guard)

