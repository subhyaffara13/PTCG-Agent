
def _serialize_secret(value: Secret[SecretType], info: core_schema.SerializationInfo) -> str | Secret[SecretType]:
    if info.mode == 'json':
        return str(value)
    else:
        return value

