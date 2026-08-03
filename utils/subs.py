import subprocess
from typing import Union

def subs(cmd: Union[list[str], str]) -> str | None:
    """
    get data from commands that we need to run outside of python
    """
    try:
        stdout = subprocess.check_output(cmd)  # noqa: S603
        return stdout.decode("utf-8", "replace").strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def subs(a, b):
    """ Replace expressions exactly """
    def subs_rl(expr):
        if expr == a:
            return b
        else:
            return expr
    return subs_rl


def subs(d, **kwargs):
    """ Full simultaneous exact substitution.

    Examples
    ========

    >>> from sympy.strategies.tools import subs
    >>> from sympy import Basic, S
    >>> mapping = {S(1): S(4), S(4): S(1), Basic(S(5)): Basic(S(6), S(7))}
    >>> expr = Basic(S(1), Basic(S(2), S(3)), Basic(S(4), Basic(S(5))))
    >>> subs(mapping)(expr)
    Basic(4, Basic(2, 3), Basic(1, Basic(6, 7)))
    """
    if d:
        return top_down(do_one(*map(rl.subs, *zip(*d.items()))), **kwargs)
    else:
        return lambda x: x

