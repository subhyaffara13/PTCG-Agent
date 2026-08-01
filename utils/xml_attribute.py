
def xml_attribute() -> Callable[[_F], _F]:
    """Decorator"""

    def decorate(f: _F) -> _F:
        _logger.debug('Registering %s.%s as XML attribute', f.__module__, f.__qualname__)
        ObjectMetadataLibrary.register_xml_property_attribute(qual_name=f'{f.__module__}.{f.__qualname__}')
        return f

    return decorate

