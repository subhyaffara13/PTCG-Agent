
def _public_version(version: Version) -> Version:
    if version.local is None:
        return version
    return version.__replace__(local=None)


def _public_version(version: Version) -> Version:
    return version.__replace__(local=None)


def _public_version(version: Version) -> Version:
    if version.local is None:
        return version
    return version.__replace__(local=None)

