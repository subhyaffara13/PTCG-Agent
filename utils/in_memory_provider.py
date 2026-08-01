
def in_memory_provider(
    config: OpenTelemetryV2Config | None = None,
) -> tuple[TracerProvider, InMemorySpanExporter]:
    """Convenience for tests: a provider exporting to an in-memory buffer."""
    cfg = config or OpenTelemetryV2Config(exporter="in_memory")
    exporter = InMemorySpanExporter()
    provider = build_tracer_provider(cfg, exporter=exporter)
    return provider, exporter

