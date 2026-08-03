import os

def high_memory(pytestconfig):
    from matplotlib.testing import is_ci_environment
    if not (os.environ.get('MPL_TEST_EXPENSIVE') or is_ci_environment()):
        pytest.skip('Test uses too much memory')

