
def test_array_api_entry_point():
    """
    Entry point for Array API implementation can be found with importlib and
    returns the main numpy namespace.
    """
    # For a development install that did not go through meson-python,
    # the entrypoint will not have been installed. So ensure this test fails
    # only if numpy is inside site-packages.
    numpy_in_sitepackages = sysconfig.get_path('platlib') in np.__file__

    eps = importlib.metadata.entry_points()
    xp_eps = eps.select(group="array_api")
    if len(xp_eps) == 0:
        if numpy_in_sitepackages:
            msg = "No entry points for 'array_api' found"
            raise AssertionError(msg) from None
        return

    try:
        ep = next(ep for ep in xp_eps if ep.name == "numpy")
    except StopIteration:
        if numpy_in_sitepackages:
            msg = "'numpy' not in array_api entry points"
            raise AssertionError(msg) from None
        return

    if ep.value == 'numpy.array_api':
        # Looks like the entrypoint for the current numpy build isn't
        # installed, but an older numpy is also installed and hence the
        # entrypoint is pointing to the old (no longer existing) location.
        # This isn't a problem except for when running tests with `spin` or an
        # in-place build.
        return

    xp = ep.load()
    msg = (
        f"numpy entry point value '{ep.value}' "
        "does not point to our Array API implementation"
    )
    assert xp is numpy, msg

