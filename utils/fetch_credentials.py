
def fetch_credentials(
    service_key: Optional[Union[str, dict]] = None,
    profile: Optional[str] = None,
    **kwargs,
) -> Dict[str, str]:
    """
    Resolution order (first-source-wins):

    Sources are checked in this order:
      kwargs
      > service key
      > env (AICORE_<NAME>)
      > config (AICORE_<NAME> or plain <name>)
      > vcap service key
      > default

    Important:
      - Credentials are extracted from the FIRST source that provides any credential value.
      - Values are NOT merged per key across sources. Except resource_group, which is merged.

    Warning:
      - This function does NOT validate the returned credentials just parsed it from the sources.
      - Callers MUST explicitly call validate_credentials() on the returned dict
    """
    config = init_conf(profile)

    service_key = _parse_service_key_once(
        service_key or litellm.sap_service_key or os.environ.get(SERVICE_KEY_ENV_VAR)
    )
    vcap_service = _get_vcap_service(VCAP_AICORE_SERVICE_NAME)

    sources = [
        Source("kwargs", lambda cv: _str_or_none(kwargs.get(cv.name))),
        Source(
            "service key",
            lambda cv: _resolve_credential_from_service_key(service_key, cv),
        ),
        Source(
            "environment variables",
            lambda cv: _str_or_none(os.environ.get(f"AICORE_{cv.name.upper()}")),
        ),
        Source(
            "config file",
            lambda cv: _str_or_none(
                config.get(f"AICORE_{cv.name.upper()}")
                if config.get(f"AICORE_{cv.name.upper()}") is not None
                else config.get(cv.name)
            ),
        ),
        Source(
            "VCAP service",
            lambda cv: (
                _str_or_none(
                    _get_nested(
                        vcap_service,
                        (("credentials",) + cv.vcap_key) if cv.vcap_key else (cv.name,),
                    )
                )
                if vcap_service
                else None
            ),
        ),  # type: ignore[arg-type]
    ]

    credentials = resolve_credentials(sources)

    resource_group = resolve_resource_group(sources)
    if resource_group is not None:
        credentials["resource_group"] = resource_group

    if "cert_url" in credentials:
        credentials["auth_url"] = credentials.pop("cert_url")
    return credentials

