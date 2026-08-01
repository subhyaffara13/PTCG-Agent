
def _configured_region(region: str | None) -> str | None:
    configured = region or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    return configured.strip() if configured is not None and configured.strip() else None

