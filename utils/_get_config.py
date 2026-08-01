
def _get_config(numels: dict[str, int]) -> dict[str, int]:
    """
    Convert numels ("x", "r0_", etc.) to block sizes ("XBLOCK", "R0_BLOCK"), etc.
    """

    return {prefix.upper() + "BLOCK": numel for prefix, numel in numels.items()}


def _get_config() -> Optional["OTelConfig"]:
    """
    Get the OTel configuration from the observability manager.

    Returns:
        OTelConfig instance if observability is enabled, None otherwise
    """
    try:
        manager = get_observability_instance().get_provider_manager()
        if manager is None:
            return None
        return manager.config
    except Exception:
        return None


def _get_config(provider: str) -> BaseSandboxConfig:
    config = ProviderConfigManager.get_provider_sandbox_config(
        SandboxProviders(provider)
    )
    if config is None:
        raise ValueError(f"Code execution is not supported for provider: {provider}")
    return config

