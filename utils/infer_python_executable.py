
def infer_python_executable(options: Options, special_opts: argparse.Namespace) -> None:
    """Infer the Python executable from the given version.

    This function mutates options based on special_opts to infer the correct Python executable
    to use.
    """
    # TODO: (ethanhs) Look at folding these checks and the site packages subprocess calls into
    # one subprocess call for speed.

    # Use the command line specified executable, or fall back to one set in the
    # config file. If an executable is not specified, infer it from the version
    # (unless no_executable is set)
    python_executable = special_opts.python_executable or options.python_executable

    if python_executable is None:
        if not special_opts.no_executable and not options.no_site_packages:
            python_executable = _python_executable_from_version(options.python_version)
    options.python_executable = python_executable

