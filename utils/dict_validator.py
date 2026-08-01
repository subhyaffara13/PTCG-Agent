
def dict_validator(v: Any) -> Dict[Any, Any]:
    if isinstance(v, dict):
        return v

    try:
        return dict(v)
    except (TypeError, ValueError):
        raise errors.DictError()

