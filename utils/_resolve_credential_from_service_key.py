
def _resolve_credential_from_service_key(
    service_key: Optional[Union[str, dict]], cv: CredentialsValue
) -> Optional[str]:
    if service_key is None:
        return None
    val = _str_or_none(
        _get_nested(
            service_key, (("credentials",) + cv.vcap_key) if cv.vcap_key else (cv.name,)
        )
    )
    if val is None:
        return _str_or_none(
            _get_nested(service_key, cv.vcap_key if cv.vcap_key else (cv.name,))
        )
    return val

