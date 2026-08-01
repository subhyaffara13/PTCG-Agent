
def should_update_prisma_schema(
    disable_updates: Union[bool, str] | None = None,
) -> bool:
    """
    Determines if Prisma Schema updates should be applied during startup.

    Args:
        disable_updates: Controls whether schema updates are disabled.
            Accepts boolean or string ('true'/'false'). Defaults to checking DISABLE_SCHEMA_UPDATE env var.

    Returns:
        bool: True if schema updates should be applied, False if updates are disabled.

    Examples:
        >>> should_update_prisma_schema()  # Checks DISABLE_SCHEMA_UPDATE env var
        >>> should_update_prisma_schema(True)  # Explicitly disable updates
        >>> should_update_prisma_schema("false")  # Enable updates using string
    """
    if disable_updates is None:
        disable_updates = os.getenv("DISABLE_SCHEMA_UPDATE", "false")

    if isinstance(disable_updates, str):
        disable_updates = str_to_bool(disable_updates)

    return not bool(disable_updates)

