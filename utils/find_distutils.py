
def find_distutils(venv, imports='distutils', env=None, **kwargs):
    py_cmd = 'import {imports}; print(distutils.__file__)'.format(**locals())
    cmd = ['python', '-c', py_cmd]
    return venv.run(cmd, env=win_sr(env), **_TEXT_KWARGS, **kwargs)

