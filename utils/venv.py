
def venv(tmp_path, setuptools_wheel):
    """Virtual env with the version of setuptools under test installed"""
    env = environment.VirtualEnv()
    env.root = path.Path(tmp_path / 'venv')
    env.create_opts = ['--no-setuptools', '--wheel=bundle']
    # TODO: Use `--no-wheel` when setuptools implements its own bdist_wheel
    env.req = str(setuptools_wheel)
    # In some environments (eg. downstream distro packaging),
    # where tox isn't used to run tests and PYTHONPATH is set to point to
    # a specific setuptools codebase, PYTHONPATH will leak into the spawned
    # processes.
    # env.create() should install the just created setuptools
    # wheel, but it doesn't if it finds another existing matching setuptools
    # installation present on PYTHONPATH:
    # `setuptools is already installed with the same version as the provided
    # wheel. Use --force-reinstall to force an installation of the wheel.`
    # This prevents leaking PYTHONPATH to the created environment.
    with contexts.environment(PYTHONPATH=None):
        return env.create()

