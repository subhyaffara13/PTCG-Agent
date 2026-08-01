
def _serialize_secret_field(
    value: _SecretField[SecretType], info: core_schema.SerializationInfo
) -> str | _SecretField[SecretType]:
    if info.mode == 'json':
        # we want the output to always be string without the `b'` prefix for bytes,
        # hence we just use `secret_display`
        return _secret_display(value.get_secret_value())
    else:
        return value

