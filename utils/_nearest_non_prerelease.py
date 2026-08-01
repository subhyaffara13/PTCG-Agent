
def _nearest_non_prerelease(
    v: _VersionOrBoundary,
) -> Version | None:
    """Smallest non-pre-release version at or above *v*, or None."""
    if v is None:
        return None
    if isinstance(v, _BoundaryVersion):
        inner = v.version
        if inner.is_prerelease:
            # AFTER_LOCALS(1.0a1) -> nearest non-pre is 1.0
            return inner.__replace__(pre=None, dev=None, local=None)
        # AFTER_LOCALS(1.0) -> nearest non-pre is 1.0.post0
        # AFTER_LOCALS(1.0.post0) -> nearest non-pre is 1.0.post1
        k = (inner.post + 1) if inner.post is not None else 0
        return inner.__replace__(post=k, local=None)
    if not v.is_prerelease:
        return v
    # Strip pre/dev to get the final or post-release form.
    return v.__replace__(pre=None, dev=None, local=None)


def _nearest_non_prerelease(
    v: _VersionOrBoundary,
) -> Version | None:
    """Smallest non-pre-release version at or above *v*, or None."""
    if v is None:
        return None
    if isinstance(v, _BoundaryVersion):
        inner = v.version
        if inner.is_prerelease:
            # AFTER_LOCALS(1.0a1) -> nearest non-pre is 1.0
            return inner.__replace__(pre=None, dev=None, local=None)
        # AFTER_LOCALS(1.0) -> nearest non-pre is 1.0.post0
        # AFTER_LOCALS(1.0.post0) -> nearest non-pre is 1.0.post1
        k = (inner.post + 1) if inner.post is not None else 0
        return inner.__replace__(post=k, local=None)
    if not v.is_prerelease:
        return v
    # Strip pre/dev to get the final or post-release form.
    return v.__replace__(pre=None, dev=None, local=None)

