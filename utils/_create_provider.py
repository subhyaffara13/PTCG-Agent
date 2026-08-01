
def _create_provider(definition: _ProviderDefinition) -> _Provider:  # pyright: ignore[reportUnusedFunction]
    provider = _Provider()
    _provider_definitions[provider] = definition
    return provider

