
def _base_version(version: Version) -> Version:
    return version.__replace__(pre=None, post=None, dev=None, local=None)

