from typing import Any

def build_metric_reader(config: OpenTelemetryV2Config) -> "MetricReader":
    """Build a metric reader mirroring v1's exporter selection.

    ``console`` (and any unrecognized kind) exports to the console; ``otlp_http``
    and ``otlp_grpc`` export over OTLP with the configured endpoint/headers. The
    reader exports on a 5s period, matching v1.
    """
    from opentelemetry.sdk.metrics.export import (
        ConsoleMetricExporter,
        PeriodicExportingMetricReader,
    )

    kind = (config.exporter or "console").lower()
    if kind in ("otlp_http", "http", "http/protobuf", "http/json"):
        from opentelemetry.exporter.otlp.proto.http.metric_exporter import (
            OTLPMetricExporter as HTTPMetricExporter,
        )
        from opentelemetry.sdk.metrics import Histogram
        from opentelemetry.sdk.metrics.export import AggregationTemporality

        exporter: Any = HTTPMetricExporter(
            endpoint=_otlp_metrics_endpoint(config.endpoint),
            headers=parse_headers(config.headers),
            preferred_temporality={Histogram: AggregationTemporality.DELTA},
        )
    elif kind in ("otlp_grpc", "grpc"):
        from opentelemetry.sdk.metrics import Histogram
        from opentelemetry.sdk.metrics.export import AggregationTemporality

        try:
            from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
                OTLPMetricExporter as GRPCMetricExporter,
            )
        except ImportError as exc:
            raise ImportError(
                "OpenTelemetry OTLP gRPC metric exporter is not available. Install "
                "`opentelemetry-exporter-otlp` and `grpcio` (or `litellm[grpc]`)."
            ) from exc

        exporter = GRPCMetricExporter(
            endpoint=config.endpoint,
            headers=parse_headers(config.headers),
            preferred_temporality={Histogram: AggregationTemporality.DELTA},
        )
    else:
        exporter = ConsoleMetricExporter()

    return PeriodicExportingMetricReader(exporter, export_interval_millis=5000)

