import pathlib
import sys

def test_warn_external(recwarn):
    _api.warn_external("oops")
    assert len(recwarn) == 1
    if sys.version_info[:2] >= (3, 12):
        # With Python 3.12, we let Python figure out the stacklevel using the
        # `skip_file_prefixes` argument, which cannot exempt tests, so just confirm
        # the filename is not in the package.
        basedir = pathlib.Path(__file__).parents[2]
        assert not recwarn[0].filename.startswith((str(basedir / 'matplotlib'),
                                                   str(basedir / 'mpl_toolkits')))
    else:
        # On older Python versions, we manually calculated the stacklevel, and had an
        # exception for our own tests.
        assert recwarn[0].filename == __file__

