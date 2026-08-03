import sys

def test_runtime_module():
    from types import ModuleType
    modname = '__runtime__'
    runtime = ModuleType(modname)
    runtime.x = 42

    mod = dill.session._stash_modules(runtime)
    if mod is not runtime:
        print("There are objects to save by referenece that shouldn't be:",
              mod.__dill_imported, mod.__dill_imported_as, mod.__dill_imported_top_level,
              file=sys.stderr)

    # This is also for code coverage, tests the use case of dump_module(refimported=True)
    # without imported objects in the namespace. It's a contrived example because
    # even dill can't be in it.  This should work after fixing #462.
    session_buffer = BytesIO()
    dill.dump_module(session_buffer, module=runtime, refimported=True)
    session_dump = session_buffer.getvalue()

    # Pass a new runtime created module with the same name.
    runtime = ModuleType(modname)  # empty
    return_val = dill.load_module(BytesIO(session_dump), module=runtime)
    assert return_val is None
    assert runtime.__name__ == modname
    assert runtime.x == 42
    assert runtime not in sys.modules.values()

    # Pass nothing as main.  load_module() must create it.
    session_buffer.seek(0)
    runtime = dill.load_module(BytesIO(session_dump))
    assert runtime.__name__ == modname
    assert runtime.x == 42
    assert runtime not in sys.modules.values()

