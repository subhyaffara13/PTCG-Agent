from typing import Callable

def type_mapping(type_: type) -> Callable[[_F], _F]:
    """Decorator"""

    def decorate(f: _F) -> _F:
        _logger.debug('Registering %s.%s with custom type: %s', f.__module__, f.__qualname__, type_)
        ObjectMetadataLibrary.register_property_type_mapping(
            qual_name=f'{f.__module__}.{f.__qualname__}', mapped_type=type_
        )
        return f

    return decorate

