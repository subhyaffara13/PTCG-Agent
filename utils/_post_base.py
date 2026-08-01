
def _post_base(version: Version) -> Version:
    """The version that *version* is a post-release of.

    1.0.post1 -> 1.0, 1.0a1.post0 -> 1.0a1, 1.0.post0.dev1 -> 1.0.
    """
    return version.__replace__(post=None, dev=None, local=None)


def _post_base(version: Version) -> Version:
    """The version that *version* is a post-release of.

    1.0.post1 -> 1.0, 1.0a1.post0 -> 1.0a1, 1.0.post0.dev1 -> 1.0.
    """
    return version.__replace__(post=None, dev=None, local=None)

