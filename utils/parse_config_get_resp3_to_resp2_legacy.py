
def parse_config_get_resp3_to_resp2_legacy(response, **options):
    """RESP3-wire CONFIG GET → today's RESP2 ``dict[str, str]`` shape.

    On RESP3 the server returns a map; convert both keys and values via
    ``str_if_bytes`` so callers using ``r.config_get()["timeout"]``
    keep working when the wire is RESP3 with ``legacy_responses=True``.
    """
    if not response:
        return {}
    return {
        str_if_bytes(key) if key is not None else None: (
            str_if_bytes(value) if value is not None else None
        )
        for key, value in response.items()
    }

