
def show_compilers() -> None:
    """Print list of available compilers (used by the "--help-compiler"
    options to "build", "build_ext", "build_clib").
    """
    # XXX this "knows" that the compiler option it's describing is
    # "--compiler", which just happens to be the case for the three
    # commands that use it.
    from distutils.fancy_getopt import FancyGetopt

    compilers = sorted(
        ("compiler=" + compiler, None, compiler_class[compiler][2])
        for compiler in compiler_class.keys()
    )
    pretty_printer = FancyGetopt(compilers)
    pretty_printer.print_help("List of available compilers:")

