
def _get_flag_names(cmd: Command, *, exclude: set[str] | None = None) -> list[str]:
    """Return long-form flag names (--foo) for optional, non-internal params.

    Boolean flags are bare ('--dry-run').  Value-taking options include a type hint ('--include TEXT', '--max-workers INTEGER').
    Synthetic global formatting flags are appended for commands that accept them.
    """
    flags: list[str] = []
    for p, long_name, _short in _iter_optional_params(cmd):
        if exclude and long_name in exclude:
            continue
        if getattr(p, "is_flag", False):
            flags.append(long_name)
        else:
            type_name = _type_hint(p)
            flags.append(f"{long_name} {type_name}")
    if _accepts_global_format_flags(cmd):
        flags.extend(flag for flag in _GLOBAL_FORMAT_INLINE_FLAGS if not (exclude and flag.split()[0] in exclude))
    return flags

