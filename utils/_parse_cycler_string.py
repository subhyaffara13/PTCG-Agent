
def _parse_cycler_string(s):
    """
    Parse a string representation of a cycler into a Cycler object safely,
    without using eval().

    Accepts expressions like::

        cycler('color', ['r', 'g', 'b'])
        cycler('color', 'rgb') + cycler('linewidth', [1, 2, 3])
        cycler(c='rgb', lw=[1, 2, 3])
        cycler('c', 'rgb') * cycler('linestyle', ['-', '--'])
    """
    try:
        tree = ast.parse(s, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Could not parse {s!r}: {e}") from e
    return _eval_cycler_expr(tree.body)

