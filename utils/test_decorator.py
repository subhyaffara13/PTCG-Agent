import functools
import sys

def test_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs) + 1

    return wrapper


def test_decorator():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=DeprecationWarning)
        # with unindentation of parameters
        decorator = doccer.filldoc(doc_dict, True)

        @decorator
        def func():
            """ Docstring
            %(strtest3)s
            """

        def expected():
            """ Docstring
            Another test
               with some indent
            """
        assert_equal(func.__doc__, expected.__doc__)

        # without unindentation of parameters

        # The docstring should be unindented for Python 3.13+
        # because of https://github.com/python/cpython/issues/81283
        decorator = doccer.filldoc(doc_dict, False if \
                                   sys.version_info < (3, 13) else True)

        @decorator
        def func():
            """ Docstring
            %(strtest3)s
            """
        def expected():
            """ Docstring
                Another test
                   with some indent
            """
        assert_equal(func.__doc__, expected.__doc__)

