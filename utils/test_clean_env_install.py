
def test_clean_env_install(venv_without_setuptools, setuptools_wheel):
    """
    Check setuptools can be installed in a clean environment.
    """
    cmd = ["python", "-m", "pip", "install", str(setuptools_wheel)]
    venv_without_setuptools.run(cmd)

