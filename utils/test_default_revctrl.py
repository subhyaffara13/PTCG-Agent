
def test_default_revctrl():
    """
    When _default_revctrl was removed from the `setuptools.command.sdist`
    module in 10.0, it broke some systems which keep an old install of
    setuptools (Distribute) around. Those old versions require that the
    setuptools package continue to implement that interface, so this
    function provides that interface, stubbed. See #320 for details.

    This interface must be maintained until Ubuntu 12.04 is no longer
    supported (by Setuptools).
    """
    (ep,) = metadata.EntryPoints._from_text(
        """
        [setuptools.file_finders]
        svn_cvs = setuptools.command.sdist:_default_revctrl
        """
    )
    res = ep.load()
    assert hasattr(res, '__iter__')

