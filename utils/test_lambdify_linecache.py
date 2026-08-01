
def test_lambdify_linecache():
    func = lambdify(x, x + 1)
    source = 'def _lambdifygenerated(x):\n    return x + 1\n'
    assert inspect.getsource(func) == source
    filename = inspect.getsourcefile(func)
    assert filename.startswith('<lambdifygenerated-')
    assert filename in linecache.cache
    assert linecache.cache[filename] == (len(source), None, source.splitlines(True), filename)
    del func
    gc.collect()
    assert filename not in linecache.cache

