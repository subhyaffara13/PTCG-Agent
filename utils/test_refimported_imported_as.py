
def test_refimported_imported_as():
    import collections
    import concurrent.futures
    import types
    import typing
    mod = sys.modules['__test__'] = types.ModuleType('__test__')
    dill.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    mod.Dict = collections.UserDict             # select by type
    mod.AsyncCM = typing.AsyncContextManager    # select by __module__
    mod.thread_exec = dill.executor             # select by __module__ with regex

    session_buffer = BytesIO()
    dill.dump_module(session_buffer, mod, refimported=True)
    session_buffer.seek(0)
    mod = dill.load(session_buffer)
    del sys.modules['__test__']

    assert set(mod.__dill_imported_as) == {
        ('collections', 'UserDict', 'Dict'),
        ('typing', 'AsyncContextManager', 'AsyncCM'),
        ('dill', 'executor', 'thread_exec'),
    }

