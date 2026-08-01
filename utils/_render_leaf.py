
def _render_leaf(path_parts: list[str], cmd: Command) -> str:
    """Render a single leaf command as a markdown list entry."""
    help_text = (cmd.help or "").split("\n")[0].strip()
    params = _format_params(cmd)
    parts = ["hf", *path_parts] + ([params] if params else [])
    entry = f"- `{' '.join(parts)}` — {help_text}"
    flags = _get_flag_names(cmd, exclude=_INLINE_FLAG_EXCLUDE)
    if flags:
        entry += f" `[{' '.join(flags)}]`"
    return entry

