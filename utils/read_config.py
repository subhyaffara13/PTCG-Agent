
def read_config(options, args, arglist, parser):
    """Read and parse configurations.

    If a config file is specified on the command line with the
    "--config" option, then only it is used for configuration.

    Otherwise, the user configuration (~/.config/pycodestyle) and any
    local configurations in the current directory or above will be
    merged together (in that order) using the read method of
    ConfigParser.
    """
    config = configparser.RawConfigParser()

    cli_conf = options.config

    local_dir = os.curdir

    if USER_CONFIG and os.path.isfile(USER_CONFIG):
        if options.verbose:
            print('user configuration: %s' % USER_CONFIG)
        config.read(USER_CONFIG)

    parent = tail = args and os.path.abspath(os.path.commonprefix(args))
    while tail:
        if config.read(os.path.join(parent, fn) for fn in PROJECT_CONFIG):
            local_dir = parent
            if options.verbose:
                print('local configuration: in %s' % parent)
            break
        (parent, tail) = os.path.split(parent)

    if cli_conf and os.path.isfile(cli_conf):
        if options.verbose:
            print('cli configuration: %s' % cli_conf)
        config.read(cli_conf)

    pycodestyle_section = None
    if config.has_section(parser.prog):
        pycodestyle_section = parser.prog
    elif config.has_section('pep8'):
        pycodestyle_section = 'pep8'  # Deprecated
        warnings.warn('[pep8] section is deprecated. Use [pycodestyle].')

    if pycodestyle_section:
        option_list = {o.dest: o.type or o.action for o in parser.option_list}

        # First, read the default values
        (new_options, __) = parser.parse_args([])

        # Second, parse the configuration
        for opt in config.options(pycodestyle_section):
            if opt.replace('_', '-') not in parser.config_options:
                print("  unknown option '%s' ignored" % opt)
                continue
            if options.verbose > 1:
                print("  {} = {}".format(opt,
                                         config.get(pycodestyle_section, opt)))
            normalized_opt = opt.replace('-', '_')
            opt_type = option_list[normalized_opt]
            if opt_type in ('int', 'count'):
                value = config.getint(pycodestyle_section, opt)
            elif opt_type in ('store_true', 'store_false'):
                value = config.getboolean(pycodestyle_section, opt)
            else:
                value = config.get(pycodestyle_section, opt)
                if normalized_opt == 'exclude':
                    value = normalize_paths(value, local_dir)
            setattr(new_options, normalized_opt, value)

        # Third, overwrite with the command-line options
        (options, __) = parser.parse_args(arglist, values=new_options)
    return options

