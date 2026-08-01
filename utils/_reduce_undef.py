
def _reduce_undef(f):
    return (_rebuild_undef, (f.name, f._kwargs))

