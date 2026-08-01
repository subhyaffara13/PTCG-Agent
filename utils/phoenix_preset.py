
def phoenix_preset(
    *,
    config_overrides: OpenTelemetryV2Config | None = None,
) -> OpenTelemetryV2Config:
    cfg = _V1Phoenix.get_arize_phoenix_config()
    headers = cfg.otlp_auth_headers if hasattr(cfg, "otlp_auth_headers") else None
    project_name = _PhoenixSettings().project_name
    base = config_overrides or OpenTelemetryV2Config()
    return base.model_copy(
        update={
            "exporters": [
                *base.exporters,
                ExporterSpec(
                    kind=cfg.protocol if hasattr(cfg, "protocol") else "otlp_http",
                    endpoint=cfg.endpoint,
                    headers=headers,
                    owner=ExporterOwner.ARIZE_PHOENIX,
                ),
            ],
            "mapper_names": ensure_mappers(base.mapper_names, "openinference"),
            "resource_attributes": {
                **base.resource_attributes,
                "openinference.project.name": project_name,
            },
        }
    )

