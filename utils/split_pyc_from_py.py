
def split_pyc_from_py(modules: list[StubSource]) -> tuple[list[StubSource], list[StubSource]]:
    py_modules = []
    pyc_modules = []
    for mod in modules:
        if is_pyc_only(mod.path):
            pyc_modules.append(mod)
        else:
            py_modules.append(mod)
    return pyc_modules, py_modules

