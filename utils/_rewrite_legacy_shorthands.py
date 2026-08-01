
def _rewrite_legacy_shorthands(args: list[str], *, rewrite_json: bool, rewrite_quiet: bool) -> None:
    """Rewrite --json / -q / --quiet to --format ... for legacy commands.

    Used for commands like 'hf jobs ls' that still own their '--format' option.
    The rewrite lets users keep using the global shorthand while click parses
    '--format <value>' locally.
    """
    has_format_in_args = any(arg == "--format" or arg.startswith("--format=") for arg in args)

    if rewrite_json and "--json" in args:
        if has_format_in_args:
            raise click.UsageError("'--json' and '--format' are mutually exclusive.")
        idx = args.index("--json")
        args[idx : idx + 1] = ["--format", "json"]
        has_format_in_args = True

    if rewrite_quiet:
        flag = "-q" if "-q" in args else ("--quiet" if "--quiet" in args else None)
        if flag is not None:
            if has_format_in_args:
                raise click.UsageError(f"'{flag}' and '--format' are mutually exclusive.")
            idx = args.index(flag)
            args[idx : idx + 1] = ["--format", "quiet"]

