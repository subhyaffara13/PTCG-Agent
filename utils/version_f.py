
def version_f(args: argparse.Namespace) -> None:
    from .. import __version__

    print(f"wheel {__version__}")

