
def _init_extensions():
    from bandit.core import extension_loader as ext_loader

    return ext_loader.MANAGER

