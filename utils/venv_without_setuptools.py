
def venv_without_setuptools(tmp_path):
    """Virtual env without any version of setuptools installed"""
    env = environment.VirtualEnv()
    env.root = path.Path(tmp_path / 'venv_without_setuptools')
    env.create_opts = ['--no-setuptools', '--no-wheel']
    env.ensure_env()
    return env

