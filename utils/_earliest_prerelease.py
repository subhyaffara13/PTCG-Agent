
def _earliest_prerelease(version: Version) -> Version:
    """Earliest pre-release of *version*.

    1.2 -> 1.2.dev0, 1.2.post1 -> 1.2.post1.dev0.
    """
    return version.__replace__(dev=0, local=None)


def _earliest_prerelease(version: Version) -> Version:
    """Earliest pre-release of *version*.

    1.2 -> 1.2.dev0, 1.2.post1 -> 1.2.post1.dev0.
    """
    return version.__replace__(dev=0, local=None)

