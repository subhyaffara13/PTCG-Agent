import os

def get_default_cache() -> str:
    """
    Return the ``PYTHON_EGG_CACHE`` environment variable
    or a platform-relevant user cache dir for an app
    named "Python-Eggs".
    """
    return os.environ.get('PYTHON_EGG_CACHE') or _user_cache_dir(appname='Python-Eggs')

