
def are_progress_bars_disabled(name: str | None = None) -> bool:
    """
    Check if progress bars are disabled globally or for a specific group.

    This function returns whether progress bars are disabled for a given group or globally.
    It checks the `HF_HUB_DISABLE_PROGRESS_BARS` environment variable first, then the programmatic
    settings.

    Args:
        name (`str`, *optional*):
            The group name to check; if None, checks the global setting.

    Returns:
        `bool`: True if progress bars are disabled, False otherwise.
    """
    if HF_HUB_DISABLE_PROGRESS_BARS is True:
        return True

    if name is None:
        return not progress_bar_states.get("_global", True)

    while name:
        if name in progress_bar_states:
            return not progress_bar_states[name]
        name = ".".join(name.split(".")[:-1])

    return not progress_bar_states.get("_global", True)

