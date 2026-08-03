from typing import Any

def uuid_validator(v: Any, field: 'ModelField') -> UUID:
    try:
        if isinstance(v, str):
            v = UUID(v)
        elif isinstance(v, (bytes, bytearray)):
            try:
                v = UUID(v.decode())
            except ValueError:
                # 16 bytes in big-endian order as the bytes argument fail
                # the above check
                v = UUID(bytes=v)
    except ValueError:
        raise errors.UUIDError()

    if not isinstance(v, UUID):
        raise errors.UUIDError()

    required_version = getattr(field.type_, '_required_version', None)
    if required_version and v.version != required_version:
        raise errors.UUIDVersionError(required_version=required_version)

    return v

