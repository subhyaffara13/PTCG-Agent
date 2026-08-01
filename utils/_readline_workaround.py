
def _readline_workaround() -> None:
    """Ensure readline is imported early so it attaches to the correct stdio handles.

    This isn't a problem with the default GNU readline implementation, but in
    some configurations, Python uses libedit instead (on macOS, and for prebuilt
    binaries such as used by uv).

    In theory this is only needed if readline.backend == "libedit", but the
    workaround consists of importing readline here, so we already worked around
    the issue by the time we could check if we need to.
    """
    try:
        import readline  # noqa: F401
    except ImportError:
        pass

