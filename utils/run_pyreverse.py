import sys

def run_pyreverse(argv: Sequence[str] | None = None) -> NoReturn:
    """Run pyreverse.

    argv can be a sequence of strings normally supplied as arguments on the command line
    """
    from pylint.pyreverse.main import Run as PyreverseRun

    sys.exit(PyreverseRun(argv or sys.argv[1:]).run())

