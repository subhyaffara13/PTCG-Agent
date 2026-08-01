
def build_resource(config: OpenTelemetryV2Config) -> Resource:
    attributes: dict[str, str] = {"service.name": config.service_name}
    if config.deployment_environment:
        attributes["deployment.environment"] = config.deployment_environment
    attributes.update(config.resource_attributes)
    return Resource.create(attributes)

