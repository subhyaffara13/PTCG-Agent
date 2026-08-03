import functools

def wrap_pytest_function_for_tracing(pyfuncitem) -> None:
    """Change the Python function object of the given Function item by a
    wrapper which actually enters pdb before calling the python function
    itself, effectively leaving the user in the pdb prompt in the first
    statement of the function."""
    _pdb = pytestPDB._init_pdb("runcall")
    testfunction = pyfuncitem.obj

    # we can't just return `partial(pdb.runcall, testfunction)` because (on
    # python < 3.7.4) runcall's first param is `func`, which means we'd get
    # an exception if one of the kwargs to testfunction was called `func`.
    @functools.wraps(testfunction)
    def wrapper(*args, **kwargs) -> None:
        func = functools.partial(testfunction, *args, **kwargs)
        _pdb.runcall(func)

    pyfuncitem.obj = wrapper

