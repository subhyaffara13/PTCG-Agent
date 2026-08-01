
def run_symilar(argv: Sequence[str] | None = None) -> NoReturn:
    """Run symilar.

    argv can be a sequence of strings normally supplied as arguments on the command line
    """
    from pylint.checkers.symilar import Run as SymilarRun

    SymilarRun(argv or sys.argv[1:])

