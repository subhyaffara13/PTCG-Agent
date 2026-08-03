from typing import Callable

def xml_name(name: str) -> Callable[[_F], _F]:
    """Decorator"""

    def decorate(f: _F) -> _F:
        _logger.debug('Registering %s.%s with XML name: %s', f.__module__, f.__qualname__, name)
        ObjectMetadataLibrary.register_custom_xml_property_name(
            qual_name=f'{f.__module__}.{f.__qualname__}', xml_property_name=name
        )
        return f

    return decorate

