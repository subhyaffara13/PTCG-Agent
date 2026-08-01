
def get_supported_tasks() -> list[str]:
    """
    Returns a list of supported task strings.
    """
    return PIPELINE_REGISTRY.get_supported_tasks()

