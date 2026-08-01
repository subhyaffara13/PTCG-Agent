
def showhelp(config: Config) -> None:
    import textwrap

    reporter: TerminalReporter | None = config.pluginmanager.get_plugin(
        "terminalreporter"
    )
    assert reporter is not None
    tw = reporter._tw
    tw.write(config._parser.optparser.format_help())
    tw.line()
    tw.line(
        "[pytest] configuration options in the first "
        "pytest.toml|pytest.ini|tox.ini|setup.cfg|pyproject.toml file found:"
    )
    tw.line()

    columns = tw.fullwidth  # costly call
    indent_len = 24  # based on argparse's max_help_position=24
    indent = " " * indent_len
    for name in config._parser._inidict:
        help, type, _default = config._parser._inidict[name]
        if help is None:
            raise TypeError(f"help argument cannot be None for {name}")
        spec = f"{name} ({type}):"
        tw.write(f"  {spec}")
        spec_len = len(spec)
        if spec_len > (indent_len - 3):
            # Display help starting at a new line.
            tw.line()
            helplines = textwrap.wrap(
                help,
                columns,
                initial_indent=indent,
                subsequent_indent=indent,
                break_on_hyphens=False,
            )

            for line in helplines:
                tw.line(line)
        else:
            # Display help starting after the spec, following lines indented.
            tw.write(" " * (indent_len - spec_len - 2))
            wrapped = textwrap.wrap(help, columns - indent_len, break_on_hyphens=False)

            if wrapped:
                tw.line(wrapped[0])
                for line in wrapped[1:]:
                    tw.line(indent + line)

    tw.line()
    tw.line("Environment variables:")
    vars = [
        (
            "CI",
            "When set to a non-empty value, pytest knows it is running in a "
            "CI process and does not truncate summary info",
        ),
        ("BUILD_NUMBER", "Equivalent to CI"),
        ("PYTEST_ADDOPTS", "Extra command line options"),
        ("PYTEST_PLUGINS", "Comma-separated plugins to load during startup"),
        ("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "Set to disable plugin auto-loading"),
        ("PYTEST_DEBUG", "Set to enable debug tracing of pytest's internals"),
        ("PYTEST_DEBUG_TEMPROOT", "Override the system temporary directory"),
        ("PYTEST_THEME", "The Pygments style to use for code output"),
        ("PYTEST_THEME_MODE", "Set the PYTEST_THEME to be either 'dark' or 'light'"),
    ]
    for name, help in vars:
        tw.line(f"  {name:<24} {help}")
    tw.line()
    tw.line()

    tw.line("to see available markers type: pytest --markers")
    tw.line("to see available fixtures type: pytest --fixtures")
    tw.line(
        "(shown according to specified file_or_dir or current dir "
        "if not specified; fixtures with leading '_' are only shown "
        "with the '-v' option"
    )

    for warningreport in reporter.stats.get("warnings", []):
        tw.line("warning : " + warningreport.message, red=True)

