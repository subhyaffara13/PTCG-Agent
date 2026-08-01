
def _accepts_global_format_flags(cmd: Command) -> bool:
    """Return True if the leaf command accepts the global '--format' / '--json' / '-q' flags."""
    if cmd.context_settings.get("ignore_unknown_options"):
        return False
    return not _has_local_formatting_option(cmd)

