
def _next_prefix_dev0(version: Version) -> Version:
    """Smallest version in the next prefix: 1.2 -> 1.3.dev0."""
    release = (*version.release[:-1], version.release[-1] + 1)
    return Version.from_parts(epoch=version.epoch, release=release, dev=0)


def _next_prefix_dev0(version: Version) -> Version:
    """Smallest version in the next prefix: 1.2 -> 1.3.dev0."""
    release = (*version.release[:-1], version.release[-1] + 1)
    return Version.from_parts(epoch=version.epoch, release=release, dev=0)

