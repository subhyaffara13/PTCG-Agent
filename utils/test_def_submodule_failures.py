
def test_def_submodule_failures():
    sm = m.def_submodule(m, b"ScratchSubModuleName")  # Using bytes to show it works.
    assert sm.__name__ == m.__name__ + "." + "ScratchSubModuleName"
    malformed_utf8 = b"\x80"
    if env.PYPY:
        # It is not worth the effort finding a trigger for a failure when running with PyPy.
        pytest.skip("Sufficiently exercised on platforms other than PyPy.")
    else:
        # Meant to trigger PyModule_GetName() failure:
        sm_name_orig = sm.__name__
        sm.__name__ = malformed_utf8
        try:
            # We want to assert that a bad __name__ causes some kind of failure, although we do not want to exercise
            # the internals of PyModule_GetName(). Currently all supported Python versions raise SystemError. If that
            # changes in future Python versions, simply add the new expected exception types here.
            with pytest.raises(SystemError):
                m.def_submodule(sm, b"SubSubModuleName")
        finally:
            # Clean up to ensure nothing gets upset by a module with an invalid __name__.
            sm.__name__ = sm_name_orig  # Purely precautionary.
    # Meant to trigger PyImport_AddModule() failure:
    with pytest.raises(UnicodeDecodeError):
        m.def_submodule(sm, malformed_utf8)

