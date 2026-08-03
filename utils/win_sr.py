import os

def win_sr(env):
    """
    On Windows, SYSTEMROOT must be present to avoid

    > Fatal Python error: _Py_HashRandomization_Init: failed to
    > get random numbers to initialize Python
    """
    if env and platform.system() == 'Windows':
        env['SYSTEMROOT'] = os.environ['SYSTEMROOT']
    return env

