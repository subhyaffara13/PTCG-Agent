
def test_docstring():

    def one(x, y):
        """ Docstring number one """
        return x + y

    def two(x, y):
        """ Docstring number two """
        return x + y

    def three(x, y):
        return x + y

    master_doc = 'Doc of the multimethod itself'

    f = Dispatcher('f', doc=master_doc)
    f.add((object, object), one)
    f.add((int, int), two)
    f.add((float, float), three)

    assert one.__doc__.strip() in f.__doc__
    assert two.__doc__.strip() in f.__doc__
    assert f.__doc__.find(one.__doc__.strip()) < \
        f.__doc__.find(two.__doc__.strip())
    assert 'object, object' in f.__doc__
    assert master_doc in f.__doc__

