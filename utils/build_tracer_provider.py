
def build_tracer_provider(
    config: OpenTelemetryV2Config,
    exporter: SpanExporter | None = None,
    baggage_processor: SpanProcessor | None = None,
    use_simple_processor: bool | None = None,
) -> TracerProvider:
    """Build the shared :class:`TracerProvider`.

    Attach the Baggage processor first (so identity attributes land on each
    span before any export decision), then add one ``SpanProcessor`` per
    ``config.exporters`` entry — this is what fans spans out to multiple
    backends. ``exporter`` and ``use_simple_processor`` are explicit overrides:
    pass a single exporter to attach exactly that one (used by tests).
    """
    provider = TracerProvider(resource=build_resource(config))
    if baggage_processor is None:
        baggage_processor = LiteLLMBaggageSpanProcessor(
            allowed_keys=config.baggage_promoted_keys
        )
    provider.add_span_processor(baggage_processor)

    if exporter is not None:
        provider.add_span_processor(_processor_for(exporter, use_simple_processor))
        return provider

    # ``config._normalize`` guarantees at least one spec (it folds the top-level
    # ``exporter``/``endpoint``/``headers`` fields in when ``exporters`` is empty).
    for spec in config.exporters:
        exp = _exporter_from_spec(spec)
        provider.add_span_processor(
            _processor_for(
                exp,
                (
                    spec.use_simple_processor
                    if spec.use_simple_processor is not None
                    else use_simple_processor
                ),
            )
        )
    return provider

