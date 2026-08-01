
def _emit_pkg_resources_deprecation_if_needed() -> None:
    if sys.version_info < (3, 11):
        # All pip versions supporting Python<=3.11 will support pkg_resources,
        # and pkg_resources is the default for these, so let's not bother users.
        return

    import importlib.metadata

    if hasattr(importlib.metadata, "_PIP_USE_IMPORTLIB_METADATA"):
        # The Python distributor has set the global constant, so we don't
        # warn, since it is not a user decision.
        return

    # The user has decided to use pkg_resources, so we warn.
    deprecated(
        reason="Using the pkg_resources metadata backend is deprecated.",
        replacement=(
            "to use the default importlib.metadata backend, "
            "by unsetting the _PIP_USE_IMPORTLIB_METADATA environment variable"
        ),
        gone_in="26.3",
        issue=13317,
    )

