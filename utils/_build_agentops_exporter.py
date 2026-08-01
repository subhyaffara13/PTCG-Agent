
def _build_agentops_exporter(spec: ExporterSpec) -> Any:
    """Factory for the ``agentops`` exporter kind: a lazy-auth OTLP/HTTP exporter."""
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
        OTLPSpanExporter,
    )

    class _LazyAuthAgentOpsExporter(OTLPSpanExporter):
        """OTLP/HTTP exporter that mints the AgentOps JWT on its first export.

        ``export`` runs in the ``BatchSpanProcessor`` worker thread, so the
        blocking token fetch never touches an event loop. The result is cached
        after the first attempt (success or failure) so it runs at most once.
        """

        def __init__(self, *, endpoint: str | None, api_key: str | None) -> None:
            super().__init__(endpoint=endpoint)
            self._agentops_api_key = api_key
            self._auth_resolved = False

        def _ensure_authenticated(self) -> None:
            if self._auth_resolved:
                return
            self._auth_resolved = True
            if not self._agentops_api_key:
                return
            try:
                token = _fetch_agentops_jwt(self._agentops_api_key).get("token")
                if token:
                    # ``_session`` is the requests.Session the base exporter
                    # POSTs through; updating its Authorization header is how the
                    # minted JWT reaches every subsequent export.
                    self._session.headers["Authorization"] = f"Bearer {token}"
            except Exception as e:
                verbose_logger.debug("AgentOps JWT fetch failed: %s", e)

        def export(self, spans: Any) -> Any:
            self._ensure_authenticated()
            return super().export(spans)

    options = spec.options or {}
    return _LazyAuthAgentOpsExporter(
        endpoint=spec.endpoint, api_key=options.get("api_key")
    )

