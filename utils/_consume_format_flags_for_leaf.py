
def _consume_format_flags_for_leaf(cmd: click.Command, args: list[str]) -> None:
    """Apply global formatting flags from 'args' to a leaf command.

    Two modes, depending on the command:

    * **Pass-through commands** (ignore_unknown_options=True, e.g. 'hf extensions exec'):
      args are forwarded verbatim to an external binary; we don't touch them.

    * **Legacy commands with a local --format option** (e.g. 'hf jobs ls' whose '--format' accepts Go templates):
      the global flags are rewritten in-place to the legacy form ('--json' → '--format json', '--quiet'/'-q' → '--format quiet'
      when the cmd has no own '--quiet') so click can parse them locally. This preserves backwards compatibility with the previous shorthand behavior.

    * **Modern commands** (no local format/quiet/json options): the flags '--format <value>' / '--json' / '--quiet' / '-q' are stripped from 'args' and applied to the singleton 'out'.

    '--no-truncate' is stripped for all non-pass-through commands; when present, human table cells are not truncated.

    Raises click.UsageError if multiple conflicting flags are supplied (e.g. '--json' together with '--format table').
    """
    if cmd.context_settings.get("ignore_unknown_options"):
        return

    no_truncate = _consume_no_truncate_flags(args)
    out.set_no_truncate(no_truncate)

    has_local_format = False
    has_local_quiet = False
    has_local_json = False
    for param in cmd.params:
        if not isinstance(param, click.Option):
            continue
        opts = (*param.opts, *param.secondary_opts)
        if "--format" in opts:
            has_local_format = True
        if "--quiet" in opts or "-q" in opts:
            has_local_quiet = True
        if "--json" in opts:
            has_local_json = True

    if has_local_format:
        _rewrite_legacy_shorthands(args, rewrite_json=not has_local_json, rewrite_quiet=not has_local_quiet)
        return

    # Strip --format/--json/-q/--quiet from 'args' and apply to 'out'
    chosen_mode: OutputFormat = OutputFormat.auto
    chosen_flag: str | None = None

    def _check_conflict(new_flag: str) -> None:
        # Reject any second formatting flag before parsing values, so the user gets
        # a "mutually exclusive" error rather than e.g. an "invalid value" error
        # from the second flag's argument.
        if chosen_flag is not None:
            raise click.UsageError(f"'{chosen_flag}' and '{new_flag}' are mutually exclusive.")

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--":
            break  # everything after '--' is a positional literal
        if arg == "--format":
            _check_conflict("--format")
            if i + 1 >= len(args):
                raise click.UsageError("Option '--format' requires a value.")
            chosen_mode = _parse_format_value(args[i + 1])
            chosen_flag = "--format"
            del args[i : i + 2]  # --format value => 2 args removed
            continue
        if arg.startswith("--format="):
            _check_conflict("--format")
            chosen_mode = _parse_format_value(arg[len("--format=") :])
            chosen_flag = "--format"
            del args[i : i + 1]
            continue
        if arg == "--json":
            _check_conflict("--json")
            chosen_mode = OutputFormat.json
            chosen_flag = "--json"
            del args[i : i + 1]
            continue
        if arg in ("-q", "--quiet"):
            _check_conflict(arg)
            chosen_mode = OutputFormat.quiet
            chosen_flag = arg
            del args[i : i + 1]
            continue
        i += 1

    out.set_mode(chosen_mode)

