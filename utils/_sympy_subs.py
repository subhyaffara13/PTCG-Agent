from typing import Any

def _sympy_subs(expr: sympy.Basic, replacements: dict[sympy.Expr, Any]) -> sympy.Basic:
    """
    When the passed replacement symbol v is a string, it is converted to a symbol with name v that
    have the same replaced expression integer and nonnegative properties.
    """

    def to_symbol(replaced: sympy.Expr, replacement: sympy.Expr | str) -> sympy.Symbol:
        if not isinstance(replaced, sympy.Expr):
            raise AssertionError(
                f"Expected sympy.Expr key, got {type(replaced)}: {replaced}"
            )
        if isinstance(replacement, str):
            return sympy.Symbol(
                replacement,
                integer=replaced.is_integer,  # type: ignore[attr-defined]
                nonnegative=replaced.is_nonnegative,  # type: ignore[attr-defined]
            )
        else:
            return replacement

    # xreplace is faster than subs, but is way more picky
    return sympy.sympify(expr).xreplace(
        {k: to_symbol(k, v) for k, v in replacements.items()}
    )

