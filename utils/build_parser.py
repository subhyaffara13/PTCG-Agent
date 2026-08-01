
def build_parser() -> optparse.OptionParser:
    """
    Return a parser for parsing requirement lines
    """
    parser = optparse.OptionParser(
        add_help_option=False,
        # override this otherwise, pytest or the name of the current running main
        # will show up in exceptions
        prog="pip_requirements_parser",
    )
    parser.print_usage = print_usage

    option_factories = SUPPORTED_OPTIONS + SUPPORTED_OPTIONS_REQ + LEGACY_OPTIONS
    for option_factory in option_factories:
        option = option_factory()
        parser.add_option(option)

    # By default optparse sys.exits on parsing errors. We want to wrap
    # that in our own exception.
    def parser_exit(self: Any, msg: str) -> "NoReturn":
        raise OptionParsingError(msg)

    # NOTE: mypy disallows assigning to a method
    #       https://github.com/python/mypy/issues/2427
    parser.exit = parser_exit  # type: ignore

    return parser


def build_parser(output_dir=dir_autolev_antlr):
    check_antlr_version()

    debug("Updating ANTLR-generated code in {}".format(output_dir))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, "__init__.py"), "w+") as fp:
        fp.write(header)

    args = [
        "antlr4",
        grammar_file,
        "-o", output_dir,
        "-no-visitor",
    ]

    debug("Running code generation...\n\t$ {}".format(" ".join(args)))
    subprocess.check_output(args, cwd=output_dir)

    debug("Applying headers, removing unnecessary files and renaming...")
    # Handle case insensitive file systems. If the files are already
    # generated, they will be written to autolev* but Autolev*.* won't match them.
    for path in (glob.glob(os.path.join(output_dir, "Autolev*.*")) or
        glob.glob(os.path.join(output_dir, "autolev*.*"))):

        # Remove files ending in .interp or .tokens as they are not needed.
        if not path.endswith(".py"):
            os.unlink(path)
            continue

        new_path = os.path.join(output_dir, os.path.basename(path).lower())
        with open(path, 'r') as f:
            lines = [line.rstrip().replace('AutolevParser import', 'autolevparser import') +'\n'
                     for line in f]

        os.unlink(path)

        with open(new_path, "w") as out_file:
            offset = 0
            while lines[offset].startswith('#'):
                offset += 1
            out_file.write(header)
            out_file.writelines(lines[offset:])

        debug("\t{}".format(new_path))

    return True


def build_parser(output_dir=dir_latex_antlr):
    check_antlr_version()

    debug("Updating ANTLR-generated code in {}".format(output_dir))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(os.path.join(output_dir, "__init__.py"), "w+") as fp:
        fp.write(header)

    args = [
        "antlr4",
        grammar_file,
        "-o", output_dir,
        # for now, not generating these as latex2sympy did not use them
        "-no-visitor",
        "-no-listener",
    ]

    debug("Running code generation...\n\t$ {}".format(" ".join(args)))
    subprocess.check_output(args, cwd=output_dir)

    debug("Applying headers, removing unnecessary files and renaming...")
    # Handle case insensitive file systems. If the files are already
    # generated, they will be written to latex* but LaTeX*.* won't match them.
    for path in (glob.glob(os.path.join(output_dir, "LaTeX*.*")) or
        glob.glob(os.path.join(output_dir, "latex*.*"))):

        # Remove files ending in .interp or .tokens as they are not needed.
        if not path.endswith(".py"):
            os.unlink(path)
            continue

        new_path = os.path.join(output_dir, os.path.basename(path).lower())
        with open(path, 'r') as f:
            lines = [line.rstrip() + '\n' for line in f]

        os.unlink(path)

        with open(new_path, "w") as out_file:
            offset = 0
            while lines[offset].startswith('#'):
                offset += 1
            out_file.write(header)
            out_file.writelines(lines[offset:])

        debug("\t{}".format(new_path))

    return True


def build_parser() -> optparse.OptionParser:
    """
    Return a parser for parsing requirement lines
    """
    parser = optparse.OptionParser(add_help_option=False)

    option_factories = SUPPORTED_OPTIONS + SUPPORTED_OPTIONS_REQ
    for option_factory in option_factories:
        option = option_factory()
        parser.add_option(option)

    # By default optparse sys.exits on parsing errors. We want to wrap
    # that in our own exception.
    def parser_exit(self: Any, msg: str) -> NoReturn:
        raise OptionParsingError(msg)

    # NOTE: mypy disallows assigning to a method
    #       https://github.com/python/mypy/issues/2427
    parser.exit = parser_exit  # type: ignore

    return parser

