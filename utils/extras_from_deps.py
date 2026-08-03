import functools

def extras_from_deps(deps):
    """
    >>> extras_from_deps(['requests'])
    set()
    >>> extras_from_deps(['pytest; extra == "test"'])
    {'test'}
    >>> sorted(extras_from_deps([
    ...     'requests',
    ...     'pytest; extra == "test"',
    ...     'pytest-cov; extra == "test"',
    ...     'sphinx; extra=="doc"']))
    ['doc', 'test']
    """
    return functools.reduce(operator.or_, map(extras_from_dep, deps), set())

