
def get_tracer(provider: TracerProvider, name: str = "litellm") -> Tracer:
    # Stamp the instrumentation scope with the LiteLLM package version so every
    # emitted span carries a deterministic ``scope.version`` (the standard OTel
    # location for the emitting library's version) for downstream consumers.
    return provider.get_tracer(name, litellm_version)

