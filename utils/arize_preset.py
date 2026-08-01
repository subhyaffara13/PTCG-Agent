
def arize_preset(
    *,
    config_overrides: OpenTelemetryV2Config | None = None,
) -> OpenTelemetryV2Config:
    arize_cfg = _V1ArizeLogger.get_arize_config()
    headers = _arize_headers(arize_cfg)
    base = config_overrides or OpenTelemetryV2Config()
    return base.model_copy(
        update={
            "exporters": [
                *base.exporters,
                ExporterSpec(
                    kind=arize_cfg.protocol or "otlp_grpc",
                    endpoint=arize_cfg.endpoint or "https://otlp.arize.com/v1",
                    headers=headers,
                    owner=ExporterOwner.ARIZE_AX,
                ),
            ],
            "mapper_names": ensure_mappers(base.mapper_names, "openinference"),
            "resource_attributes": {
                **base.resource_attributes,
                **(
                    {"model_id": arize_cfg.project_name}
                    if arize_cfg.project_name
                    else {}
                ),
            },
        }
    )

