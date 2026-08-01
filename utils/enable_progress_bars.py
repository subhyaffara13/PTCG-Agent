
def enable_progress_bars(name: str | None = None) -> None:
    """
    Enable progress bars either globally or for a specified group.

    This function sets the progress bars to enabled for the specified group or globally
    if no group is specified. The operation is subject to the `HF_HUB_DISABLE_PROGRESS_BARS`
    environment setting.

    Args:
        name (`str`, *optional*):
            The name of the group for which to enable the progress bars. If None,
            progress bars are enabled globally.

    Raises:
        Warning: If the environment variable precludes changes.
    """
    if HF_HUB_DISABLE_PROGRESS_BARS is True:
        warnings.warn(
            "Cannot enable progress bars: environment variable `HF_HUB_DISABLE_PROGRESS_BARS=1` is set and has priority."
        )
        return

    if name is None:
        progress_bar_states.clear()
        progress_bar_states["_global"] = True
    else:
        keys_to_remove = [key for key in progress_bar_states if key.startswith(f"{name}.")]
        for key in keys_to_remove:
            del progress_bar_states[key]
        progress_bar_states[name] = True

