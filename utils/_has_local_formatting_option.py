
def _has_local_formatting_option(cmd: click.Command) -> bool:
    """Return True if the command defines its own --format, --json or --quiet / -q.

    Used to skip the global formatting flag pre-processor and the duplicated "Formatting options" help section for
    legacy commands like 'hf jobs ls' that have their own format/quiet options.
    """
    for param in cmd.params:
        if not isinstance(param, click.Option):
            continue
        opts = (*param.opts, *param.secondary_opts)
        if "--format" in opts or "--json" in opts or "--quiet" in opts or "-q" in opts:
            return True
    return False

