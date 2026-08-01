
def paths_on_pythonpath(paths):
    """
    Add the indicated paths to the head of the PYTHONPATH environment
    variable so that subprocesses will also see the packages at
    these paths.

    Do this in a context that restores the value on exit.

    >>> getfixture('monkeypatch').setenv('PYTHONPATH', 'anything')
    >>> with paths_on_pythonpath(['foo', 'bar']):
    ...     assert 'foo' in os.environ['PYTHONPATH']
    ...     assert 'anything' in os.environ['PYTHONPATH']
    >>> os.environ['PYTHONPATH']
    'anything'

    >>> getfixture('monkeypatch').delenv('PYTHONPATH')
    >>> with paths_on_pythonpath(['foo', 'bar']):
    ...     assert 'foo' in os.environ['PYTHONPATH']
    >>> os.environ.get('PYTHONPATH')
    """
    nothing = object()
    orig_pythonpath = os.environ.get('PYTHONPATH', nothing)
    current_pythonpath = os.environ.get('PYTHONPATH', '')
    try:
        prefix = os.pathsep.join(unique_everseen(paths))
        to_join = filter(None, [prefix, current_pythonpath])
        new_path = os.pathsep.join(to_join)
        if new_path:
            os.environ['PYTHONPATH'] = new_path
        yield
    finally:
        if orig_pythonpath is nothing:
            os.environ.pop('PYTHONPATH', None)
        else:
            os.environ['PYTHONPATH'] = orig_pythonpath

