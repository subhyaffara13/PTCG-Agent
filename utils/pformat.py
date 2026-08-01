
def pformat(obj: t.Any) -> str:
    """Format an object using :func:`pprint.pformat`."""
    from pprint import pformat

    return pformat(obj)


def pformat(obj: Any) -> str:
    if isinstance(obj, (OrderedSet, set)):  # noqa: set_linter
        # pformat has trouble with sets of sympy exprs
        obj = sorted(obj, key=str)
    result = pprint.pformat(obj, indent=4)
    if "\n" in result:
        return f"\n{textwrap.indent(result, ' ' * 4)}"
    return result

