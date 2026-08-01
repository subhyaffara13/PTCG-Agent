
def test_distutils_local_with_setuptools(venv):
    """
    Ensure local distutils is used when appropriate.
    """
    env = dict(SETUPTOOLS_USE_DISTUTILS='local')
    loc = find_distutils(venv, imports='setuptools, distutils', env=env)
    assert venv.name in loc.split(os.sep)
    assert count_meta_path(venv, env=env) <= 1

