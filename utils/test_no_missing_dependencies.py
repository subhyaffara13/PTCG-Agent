
def test_no_missing_dependencies(bare_venv, request):
    """
    Quick and dirty test to ensure all external dependencies are vendored.
    """
    setuptools_dir = request.config.rootdir
    bare_venv.run(['python', 'setup.py', '--help'], cwd=setuptools_dir)

