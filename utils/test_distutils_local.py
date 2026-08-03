import os

def test_distutils_local(venv):
    """
    Even without importing, the setuptools-local copy of distutils is
    preferred.
    """
    env = dict(SETUPTOOLS_USE_DISTUTILS='local')
    assert venv.name in find_distutils(venv, env=env).split(os.sep)
    assert count_meta_path(venv, env=env) <= 1

