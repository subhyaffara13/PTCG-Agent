
def string_format(format_: str) -> Callable[[_F], _F]:
    """Decorator"""

    def decorate(f: _F) -> _F:
        _logger.debug('Registering %s.%s with String Format: %s', f.__module__, f.__qualname__, format_)
        ObjectMetadataLibrary.register_custom_string_format(
            qual_name=f'{f.__module__}.{f.__qualname__}', string_format=format_
        )
        return f

    return decorate

