
def pytest_virtualenv_works(venv):
    """
    pytest_virtualenv may not work. if it doesn't, skip these
    tests. See #1284.
    """
    venv_prefix = venv.run(["python", "-c", "import sys; print(sys.prefix)"]).strip()
    if venv_prefix == sys.prefix:
        pytest.skip("virtualenv is broken (see pypa/setuptools#1284)")

