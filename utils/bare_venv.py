
def bare_venv(tmp_path):
    """Virtual env without any common packages installed"""
    env = environment.VirtualEnv()
    env.root = path.Path(tmp_path / 'bare_venv')
    env.create_opts = ['--no-setuptools', '--no-pip', '--no-wheel', '--no-seed']
    env.ensure_env()
    return env

