
def _get_provider_definition(provider: _Provider) -> _ProviderDefinition:
    try:
        return _provider_definitions[provider]
    except (KeyError, TypeError) as exc:
        raise OpenAIError("Invalid provider. Providers must be created by an OpenAI provider factory.") from exc

