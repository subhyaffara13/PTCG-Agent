
def resolve_passthrough_managed_id_provider(
    custom_llm_provider: Any,
) -> Optional[str]:
    """Map a pass-through ``custom_llm_provider`` to the provider scope that
    namespaces passthrough managed object IDs, or ``None`` when the route is not
    an OpenAI/Azure pass-through and managed IDs must not apply.

    Scoping is keyed on the explicit provider that the pass-through route
    forwards (``openai``, ``azure``, ``azure_ai``), not on the upstream URL, so
    a third-party OpenAI-compatible endpoint never triggers managed-ID minting.

    ``azure`` and ``azure_ai`` deliberately collapse to one ``"azure"`` scope:
    they expose the same Azure OpenAI files/batches surface, so an ID minted
    while routing as one must still resolve while routing as the other.
    Splitting them would make a managed ID minted on ``azure`` fail to resolve
    when replayed on ``azure_ai`` and vice versa.
    """
    provider = str(
        getattr(custom_llm_provider, "value", custom_llm_provider) or ""
    ).lower()
    if not provider:
        return None
    if provider in PASSTHROUGH_MANAGED_ID_AZURE_PROVIDERS or provider.endswith(
        (".azure", ".azure_ai")
    ):
        return "azure"
    if provider == "openai" or provider.endswith(".openai"):
        return "openai"
    return None

