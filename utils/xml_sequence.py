from typing import Callable

def xml_sequence(sequence: int) -> Callable[[_F], _F]:
    """Decorator"""

    def decorate(f: _F) -> _F:
        _logger.debug('Registering %s.%s with XML sequence: %s', f.__module__, f.__qualname__, sequence)
        ObjectMetadataLibrary.register_xml_property_sequence(
            qual_name=f'{f.__module__}.{f.__qualname__}', sequence=sequence
        )
        return f

    return decorate

