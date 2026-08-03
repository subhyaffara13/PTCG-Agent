import sys

def _dedent_for_py313(s):
    """Apply textwrap.dedent to s for Python versions 3.13 or later."""
    return s if sys.version_info < (3, 13) else textwrap.dedent(s)

