
def _log_args_maybe_list(arg: object, label: str) -> None:
    if isinstance(arg, (list, tuple)):
        _log_args_list(arg, label)
    else:
        aot_graphs_log.debug("%s: %s", label, _describe_arg_for_logging(arg))

