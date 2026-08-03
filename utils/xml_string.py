from typing import Callable

def xml_string(string_type: XmlStringSerializationType) -> Callable[[_F], _F]:
    """Decorator"""

    def decorate(f: _F) -> _F:
        _logger.debug('Registering %s.%s as XML StringType: %s', f.__module__, f.__qualname__, string_type)
        ObjectMetadataLibrary.register_xml_property_string_config(
            qual_name=f'{f.__module__}.{f.__qualname__}', string_type=string_type
        )
        return f

    return decorate

