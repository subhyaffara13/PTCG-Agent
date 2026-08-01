
def agentops_preset(
    *,
    config_overrides: OpenTelemetryV2Config | None = None,
) -> OpenTelemetryV2Config:
    """Build the AgentOps config without any network I/O.

    The ``agentops`` exporter mints (and caches) the JWT lazily on its first
    export, so this stays non-blocking. ``project.id`` is therefore not a
    resource attribute — it is encoded in the JWT, which AgentOps uses to route
    the trace to the right project.
    """
    settings = _AgentOpsSettings()
    base = config_overrides or OpenTelemetryV2Config()
    return base.model_copy(
        update={
            "exporters": [
                *base.exporters,
                ExporterSpec(
                    kind=_AGENTOPS_EXPORTER_KIND,
                    endpoint=_AGENTOPS_ENDPOINT,
                    options=(
                        {"api_key": settings.api_key} if settings.api_key else None
                    ),
                    owner=ExporterOwner.AGENTOPS,
                ),
            ],
            "resource_attributes": {
                **base.resource_attributes,
                "service.name": settings.service_name,
                "telemetry.sdk.name": "agentops",
                **(
                    {"deployment.environment": settings.environment}
                    if settings.environment
                    else {}
                ),
            },
        }
    )

