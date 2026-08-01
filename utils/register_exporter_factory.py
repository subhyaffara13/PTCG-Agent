
def register_exporter_factory(
    kind: str, factory: Callable[[ExporterSpec], SpanExporter]
) -> None:
    """Register a custom exporter ``factory`` for the exporter ``kind``."""
    _EXPORTER_FACTORIES[kind.lower()] = factory

