
def _make_ext(name, docstring):
    class Foo: ...

    Foo.__doc__ = docstring
    m1 = importlib.metadata.EntryPoint(name, f'{name}_module:{name}', 'group')
    return extension.Extension(name, m1, Foo, None)

