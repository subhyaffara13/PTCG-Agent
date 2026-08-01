
def get_meter(provider: MeterProvider, name: str = "litellm") -> "Meter":
    return provider.get_meter(name, litellm_version)

