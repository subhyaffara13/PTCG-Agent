
def _promote_extra_body_to_optional_params(optional_params: dict) -> None:
    """Promote anthropic-native passthrough keys out of ``extra_body``.

    ``azure_ai`` is an OpenAI-compatible provider, so non-OpenAI kwargs like
    ``output_config`` get auto-routed into ``extra_body`` by
    ``add_provider_specific_params_to_optional_params``. For the Azure→Anthropic
    route those keys must reach the request body and be validated, so promote
    them. ``setdefault`` keeps explicit top-level values authoritative.
    """
    extra_body = optional_params.get("extra_body")
    if not isinstance(extra_body, dict) or not extra_body:
        return
    for k, v in extra_body.items():
        optional_params.setdefault(k, v)
    optional_params.pop("extra_body", None)

