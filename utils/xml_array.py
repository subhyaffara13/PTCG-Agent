
def xml_array(array_type: XmlArraySerializationType, child_name: str) -> Callable[[_F], _F]:
    """Decorator"""

    def decorate(f: _F) -> _F:
        _logger.debug('Registering %s.%s as XML Array: %s:%s', f.__module__, f.__qualname__, array_type, child_name)
        ObjectMetadataLibrary.register_xml_property_array_config(
            qual_name=f'{f.__module__}.{f.__qualname__}', array_type=array_type, child_name=child_name
        )
        return f

    return decorate

