import os
import sys

def test_open(mocker):
    with tools._open('-') as fobj:
        assert fobj is sys.stdin

    try:
        with tools._open(__file__) as fobj:
            assert True
    except TypeError:  # issue 101
        assert False, 'tools._open raised TypeError'

    m = mocker.mock_open()

    if platform.python_implementation() == 'PyPy':
        mocker.patch('radon.cli.tools.open', m, create=True)
        tools._open('randomfile.py').__enter__()
        m.assert_called_with('randomfile.py')
    else:
        mocker.patch('radon.cli.tools._open_function', m, create=True)
        tools._open('randomfile.py').__enter__()
        if sys.version_info[:2] >= (3, 0):
            default_encoding = 'utf-8'
        else:
            default_encoding = locale.getpreferredencoding(False)
        except_encoding = os.getenv(
            'RADONFILESENCODING', default_encoding
        )
        m.assert_called_with('randomfile.py', encoding=except_encoding)

