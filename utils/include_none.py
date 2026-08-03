from typing import Any, Callable, Optional

def include_none(view_: Optional[Type[ViewType]] = None, none_value: Optional[Any] = None) -> Callable[[_F], _F]:
    """Decorator"""

    def decorate(f: _F) -> _F:
        _logger.debug('Registering %s.%s to include None for view: %s', f.__module__, f.__qualname__, view_)
        ObjectMetadataLibrary.register_property_include_none(
            qual_name=f'{f.__module__}.{f.__qualname__}', view_=view_, none_value=none_value
        )
        return f

    return decorate

