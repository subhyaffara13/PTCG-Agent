
def register_artifact(
    setting_name, description, visible=False, off_by_default=False, log_format=None
) -> None:
    """
    Enables an artifact to be controlled by the env var and user API with name
    Args:
        setting_name: the shorthand name used in the env var and user API
        description: A description of what this outputs
        visible: Whether it gets suggested to users by default
        off_by_default: whether this artifact should be logged when the ancestor loggers
            are enabled at level DEBUG
    """
    log_registry.register_artifact_name(
        setting_name, description, visible, off_by_default, log_format
    )

