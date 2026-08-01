
def partial_flatten_asdict(obj: object) -> Any:
    if dataclasses.is_dataclass(obj):
        return {
            field.name: getattr(obj, field.name) for field in dataclasses.fields(obj)
        }
    elif isinstance(obj, (list, tuple)):
        return obj.__class__([partial_flatten_asdict(item) for item in obj])
    elif isinstance(obj, dict):
        return {k: partial_flatten_asdict(v) for k, v in obj.items()}
    else:
        return obj

