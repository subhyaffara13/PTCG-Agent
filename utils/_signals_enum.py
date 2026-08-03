import sys

def _signals_enum() -> str:
    """Generates the source code for the Signals int enum."""
    signals_enum = """
    import enum
    class Signals(enum.IntEnum):
        SIGABRT   = enum.auto()
        SIGEMT    = enum.auto()
        SIGFPE    = enum.auto()
        SIGILL    = enum.auto()
        SIGINFO   = enum.auto()
        SIGINT    = enum.auto()
        SIGSEGV   = enum.auto()
        SIGTERM   = enum.auto()
    """
    if sys.platform != "win32":
        signals_enum += """
        SIGALRM   = enum.auto()
        SIGBUS    = enum.auto()
        SIGCHLD   = enum.auto()
        SIGCONT   = enum.auto()
        SIGHUP    = enum.auto()
        SIGIO     = enum.auto()
        SIGIOT    = enum.auto()
        SIGKILL   = enum.auto()
        SIGPIPE   = enum.auto()
        SIGPROF   = enum.auto()
        SIGQUIT   = enum.auto()
        SIGSTOP   = enum.auto()
        SIGSYS    = enum.auto()
        SIGTRAP   = enum.auto()
        SIGTSTP   = enum.auto()
        SIGTTIN   = enum.auto()
        SIGTTOU   = enum.auto()
        SIGURG    = enum.auto()
        SIGUSR1   = enum.auto()
        SIGUSR2   = enum.auto()
        SIGVTALRM = enum.auto()
        SIGWINCH  = enum.auto()
        SIGXCPU   = enum.auto()
        SIGXFSZ   = enum.auto()
        """
    if sys.platform == "win32":
        signals_enum += """
        SIGBREAK  = enum.auto()
        """
    if sys.platform not in ("darwin", "win32"):
        signals_enum += """
        SIGCLD    = enum.auto()
        SIGPOLL   = enum.auto()
        SIGPWR    = enum.auto()
        SIGRTMAX  = enum.auto()
        SIGRTMIN  = enum.auto()
        """
    return signals_enum

