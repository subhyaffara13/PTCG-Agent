
def _exporter_from_spec(spec: ExporterSpec) -> SpanExporter:
    kind = (spec.kind or "console").lower()
    factory = _EXPORTER_FACTORIES.get(kind)
    if factory is not None:
        return factory(spec)
    if kind in ("in_memory", "inmemory", "memory"):
        return InMemorySpanExporter()
    if kind in ("otlp_http", "http", "http/protobuf", "http/json"):
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
            OTLPSpanExporter as HTTPExporter,
        )

        return HTTPExporter(
            endpoint=_otlp_traces_endpoint(spec.endpoint),
            headers=parse_headers(spec.headers),
        )
    if kind in ("otlp_grpc", "grpc"):
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
            OTLPSpanExporter as GRPCExporter,
        )

        return GRPCExporter(endpoint=spec.endpoint, headers=parse_headers(spec.headers))
    return ConsoleSpanExporter()

