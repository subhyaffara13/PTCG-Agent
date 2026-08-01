
def build_span_exporter(config: OpenTelemetryV2Config) -> SpanExporter:
    """Build a single exporter from the top-level config fields.

    Convenience for the common single-exporter case (and for tests): reads the
    ``exporter`` / ``endpoint`` / ``headers`` fields. To configure multiple
    exporters, populate ``config.exporters`` directly.
    """
    return _exporter_from_spec(
        ExporterSpec(
            kind=config.exporter, endpoint=config.endpoint, headers=config.headers
        )
    )

