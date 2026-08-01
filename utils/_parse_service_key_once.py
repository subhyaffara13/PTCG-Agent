
def _parse_service_key_once(
    service_key: Optional[Union[str, dict]],
) -> Optional[Dict[str, Any]]:
    """
    Pre-parse service_key if it's a string to avoid repeated JSON parsing.

    Returns None if parsing fails (other credential sources may still work).
    """
    if service_key is None:
        return None
    if isinstance(service_key, dict):
        return service_key
    if isinstance(service_key, str):
        try:
            return json.loads(service_key)
        except json.JSONDecodeError:
            verbose_logger.warning(
                "SAP service key is a string but not valid JSON. Skipping this source."
            )
            return None
    verbose_logger.warning(
        f"SAP service key has unexpected type '{type(service_key).__name__}'. Expected str or dict. Ignoring."
    )
    return None

