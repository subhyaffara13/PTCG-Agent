from typing import Any

def isInt(f: Any) -> int:
    try:
        i = int(f)
        if f - i == 0:
            return 1
        else:
            return 0
    except (ValueError, OverflowError):
        return 0


def is_int(x: object) -> TypeGuard[int | torch.SymInt]:
    return isinstance(x, int) or (isinstance(x, torch.SymInt) and x.node.expr.is_number)


def is_int(x: object) -> TypeIs[int]:
    return isinstance(x, Integer)


def is_int(c):
    r"""
    Test whether an argument is of an acceptable type to be used as an integer.

    Explanation
    ===========

    Returns ``True`` on any argument of type ``int`` or :ref:`ZZ`.

    See Also
    ========

    is_rat

    """
    # If gmpy2 is installed then ``ZZ.of_type()`` accepts only
    # ``mpz``, not ``int``, so we need another clause to ensure ``int`` is
    # accepted.
    return isinstance(c, int) or ZZ.of_type(c)


def is_int(dtype):
  return jnp.issubdtype(dtype, jnp.integer)

