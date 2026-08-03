import sys

def _should_suppress_build_backends() -> bool:
    return sys.version_info < (3, 12)

