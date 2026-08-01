
def resolve_meter_provider(
    config: OpenTelemetryV2Config,
    meter_provider: MeterProvider | None = None,
) -> MeterProvider:
    """Resolve the :class:`MeterProvider` GenAI metrics record through.

    An injected provider wins (DI/tests). Otherwise reuse whatever the operator has
    configured as the global, whether a real SDK provider or an explicit
    ``NoOpMeterProvider``, so the GenAI histograms ride the operator's
    readers/exporters and an explicit opt-out is honored. Only when the global is
    still the default proxy placeholder does V2 build one from the config and
    publish it as the global, mirroring how V2 owns trace export. The built
    provider is the one returned, so its reader thread is always live, never
    orphaned.
    """
    if meter_provider is not None:
        return meter_provider

    existing = metrics.get_meter_provider()
    if isinstance(existing, (SDKMeterProvider, NoOpMeterProvider)):
        return existing

    provider = build_meter_provider(config)
    metrics.set_meter_provider(provider)
    return provider

