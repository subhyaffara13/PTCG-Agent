
def has_changed(*args, **kwds):
    kwds['simple'] = True  # ignore simple if passed in
    return whats_changed(*args, **kwds)

