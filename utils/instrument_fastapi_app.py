
def instrument_fastapi_app(app: Any) -> None:
    """Attach OTel server-span instrumentation to the proxy FastAPI app.

    Safe no-op when the V2 gate is off or ``opentelemetry-instrumentation-fastapi``
    is unavailable. This MUST be called at app-creation time — once the lifespan
    runs, the middleware stack is frozen and ``instrument_app`` raises "Cannot add
    middleware after an application has started".

    No ``TracerProvider`` is passed, so the instrumentation binds to the OTel global
    ``ProxyTracerProvider``; the proxy publishes the real provider as the global
    after config load (see ``proxy_startup_event``), and the proxy delegates to it.
    That way server spans and gen-ai spans share one provider and the same trace.
    """
    try:
        if not is_otel_v2_enabled():
            return

        # Lazy: only the V2-enabled path needs the optional
        # ``opentelemetry-instrumentation-fastapi`` package, which is not part of the
        # base ``litellm[proxy]`` install. Importing it at module top would make
        # ``proxy_server``'s unconditional ``import`` of this module crash when the
        # package is absent, even with the gate off.
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

        excluded_urls = (
            os.environ.get("OTEL_PYTHON_FASTAPI_EXCLUDED_URLS")
            if "OTEL_PYTHON_FASTAPI_EXCLUDED_URLS" in os.environ
            else _DEFAULT_EXCLUDED_URLS
        )
        FastAPIInstrumentor.instrument_app(
            app,
            excluded_urls=excluded_urls,
            server_request_hook=_passthrough_span_name_hook,
            # Drop the ASGI "http receive"/"http send" lifecycle sub-spans: they
            # are low-value noise and (for passthrough) carry the catch-all route
            # template in their name, which can't be rewritten from a hook.
            exclude_spans=["receive", "send"],
        )
    except Exception as e:
        verbose_logger.debug("Skipping OTel V2 FastAPI instrumentation: %s", e)

