
def json_name(name: str) -> Callable[[_F], _F]:
    """Decorator"""

    def decorate(f: _F) -> _F:
        _logger.debug('Registering %s.%s with JSON name: %s', f.__module__, f.__qualname__, name)
        ObjectMetadataLibrary.register_custom_json_property_name(
            qual_name=f'{f.__module__}.{f.__qualname__}', json_property_name=name
        )
        return f

    return decorate


def json_name(field: str) -> str:
    return field.lower().replace("-", "_")

