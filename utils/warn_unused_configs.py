
def warn_unused_configs(
    options: Options, flush_errors: Callable[[str | None, list[str], bool], None]
) -> None:
    unused_configs = options.get_unused_configs()
    if options.warn_unused_configs and unused_configs and not options.non_interactive:
        unused = get_config_module_names(
            options.config_file,
            [glob for glob in options.per_module_options.keys() if glob in unused_configs],
        )
        flush_errors(
            None, ["{}: note: unused section(s): {}".format(options.config_file, unused)], False
        )

