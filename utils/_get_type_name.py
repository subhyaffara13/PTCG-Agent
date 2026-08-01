
def _get_type_name(x: Any) -> str:
    type_ = type(x)
    if type_ in _JSON_TYPES:
        return type_.__name__

    # Handle proper subclasses; note we don't need to handle None or bool here
    if isinstance(x, int):
        return 'int'
    if isinstance(x, float):
        return 'float'
    if isinstance(x, str):
        return 'str'
    if isinstance(x, list):
        return 'list'
    if isinstance(x, dict):
        return 'dict'

    # Fail by returning the type's actual name
    return getattr(type_, '__name__', '<no type name>')

