
def test_patching_does_not_cause_problems():
    # Ensure `dist.log` is only patched if necessary

    import _distutils_hack

    import setuptools.logging

    from distutils import dist

    setuptools.logging.configure()

    if _distutils_hack.enabled():
        # Modern logging infra, no problematic patching.
        assert dist.__file__ is None or "setuptools" in dist.__file__
        assert isinstance(dist.log, logging.Logger)
    else:
        assert inspect.ismodule(dist.log)

