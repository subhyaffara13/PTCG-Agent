
def _is_fake_dep(d):
    return isinstance(d, WeakDep) and d.is_fake

