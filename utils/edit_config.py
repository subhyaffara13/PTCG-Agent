
def edit_config(filename, settings) -> None:
    """Edit a configuration file to include `settings`

    `settings` is a dictionary of dictionaries or ``None`` values, keyed by
    command/section name.  A ``None`` value means to delete the entire section,
    while a dictionary lists settings to be changed or deleted in that section.
    A setting of ``None`` means to delete that setting.
    """
    log.debug("Reading configuration from %s", filename)
    opts = configparser.RawConfigParser()
    opts.optionxform = lambda optionstr: optionstr  # type: ignore[method-assign] # overriding method
    _cfg_read_utf8_with_fallback(opts, filename)

    for section, options in settings.items():
        if options is None:
            log.info("Deleting section [%s] from %s", section, filename)
            opts.remove_section(section)
        else:
            if not opts.has_section(section):
                log.debug("Adding new section [%s] to %s", section, filename)
                opts.add_section(section)
            for option, value in options.items():
                if value is None:
                    log.debug("Deleting %s.%s from %s", section, option, filename)
                    opts.remove_option(section, option)
                    if not opts.options(section):
                        log.info(
                            "Deleting empty [%s] section from %s", section, filename
                        )
                        opts.remove_section(section)
                else:
                    log.debug(
                        "Setting %s.%s to %r in %s", section, option, value, filename
                    )
                    opts.set(section, option, value)

    log.info("Writing %s", filename)
    with open(filename, 'w', encoding="utf-8") as f:
        opts.write(f)

