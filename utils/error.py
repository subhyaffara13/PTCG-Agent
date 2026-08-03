import sys

def error(msg):
    from cffi._shimmed_dist_utils import DistutilsSetupError
    raise DistutilsSetupError(msg)


def error(msg: str, *args: object):
    """Logs an error message if min_level <= ERROR in red on the sys.stderr."""
    if min_level <= ERROR:
        print(colorize(f"ERROR: {msg % args}", "red"), file=sys.stderr)


def error(msg: str, *args: object):
    """Logs an error message if min_level <= ERROR in red on the sys.stderr."""
    if min_level <= ERROR:
        warnings.warn(colorize(f"ERROR: {msg % args}", "red"), stacklevel=3)


def Error(msg: str) -> ParserElement:
    """Helper class to raise parser errors."""
    def raise_error(s: str, loc: int, toks: ParseResults) -> T.Any:
        raise ParseFatalException(s, loc, msg)

    return Empty().set_parse_action(raise_error)


def error() -> NoReturn:
    raise AssertionError("shouldn't be hit")


def error(msg, *args, **kwargs):
  """Logs an error message."""
  log(ERROR, msg, *args, **kwargs)

