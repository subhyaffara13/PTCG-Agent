
def _restore_dispatchable(name):
    return _registered_algorithms[name].__wrapped__

