
def _configure_provider(provider: _Provider) -> _ProviderRuntime:  # pyright: ignore[reportUnusedFunction]
    return _get_provider_definition(provider).configure()

