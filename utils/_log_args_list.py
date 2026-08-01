
def _log_args_list(args: Sequence[object], label: str) -> None:
    aot_graphs_log.debug("%s (count=%s):", label, len(args))
    for i, arg in enumerate(args):
        aot_graphs_log.debug("  [%s] %s", i, _describe_arg_for_logging(arg))

