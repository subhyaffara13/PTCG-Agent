
def test_source():
    def one(x, y):
        """ Docstring number one """
        return x + y

    def two(x, y):
        """ Docstring number two """
        return x - y

    master_doc = 'Doc of the multimethod itself'

    f = Dispatcher('f', doc=master_doc)
    f.add((int, int), one)
    f.add((float, float), two)

    assert 'x + y' in f._source(1, 1)
    assert 'x - y' in f._source(1.0, 1.0)

