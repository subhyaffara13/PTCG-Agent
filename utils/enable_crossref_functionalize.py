
def enable_crossref_functionalize() -> Generator[None, None, None]:
    for op in all_py_loaded_overloads():
        op._uncache_dispatch(torch._C.DispatchKey.Functionalize)
    try:
        with (
            enable_python_dispatcher(),
            unittest.mock.patch("torch._dispatch.python.CROSSREF_FUNCTIONALIZE", True),
        ):
            yield
    finally:
        for op in all_py_loaded_overloads():
            op._uncache_dispatch(torch._C.DispatchKey.Functionalize)

