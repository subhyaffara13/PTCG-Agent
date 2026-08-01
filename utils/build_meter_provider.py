
def build_meter_provider(
    config: OpenTelemetryV2Config,
    metric_reader: "MetricReader | None" = None,
) -> SDKMeterProvider:
    """Build the :class:`MeterProvider` for GenAI metrics.

    ``metric_reader`` is an explicit override (tests inject an
    ``InMemoryMetricReader``); otherwise the reader is selected from the config's
    exporter kind via :func:`build_metric_reader`.
    """
    reader = metric_reader if metric_reader is not None else build_metric_reader(config)
    return SDKMeterProvider(metric_readers=[reader], resource=build_resource(config))

