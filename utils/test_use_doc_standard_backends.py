
def test_use_doc_standard_backends():
    """
    Test that the standard backends mentioned in the docstring of
    matplotlib.use() are the same as in matplotlib.rcsetup.
    """
    def parse(key):
        backends = []
        for line in matplotlib.use.__doc__.split(key)[1].split('\n'):
            if not line.strip():
                break
            backends += [e.strip().lower() for e in line.split(',') if e]
        return backends

    from matplotlib.backends import BackendFilter, backend_registry

    assert (set(parse('- interactive backends:\n')) ==
            set(backend_registry.list_builtin(BackendFilter.INTERACTIVE)))
    assert (set(parse('- non-interactive backends:\n')) ==
            set(backend_registry.list_builtin(BackendFilter.NON_INTERACTIVE)))

