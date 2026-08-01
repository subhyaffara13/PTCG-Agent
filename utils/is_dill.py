
def is_dill(pickler, child=None):
    "check the dill-ness of your pickler"
    if child is False or not hasattr(pickler.__class__, 'mro'):
        return 'dill' in pickler.__module__
    return Pickler in pickler.__class__.mro()

