
def test_excluded_subpackages(tmpdir_cwd):
    jaraco.path.build(EXAMPLE_WITH_MANIFEST)
    dist = Distribution({"script_name": "%PEP 517%"})
    dist.parse_config_files()

    build_py = dist.get_command_obj("build_py")

    msg = r"Python recognizes 'mypkg\.tests' as an importable package"
    with pytest.warns(SetuptoolsDeprecationWarning, match=msg):  # noqa: PT031
        # TODO: To fix #3260 we need some transition period to deprecate the
        # existing behavior of `include_package_data`. After the transition, we
        # should remove the warning and fix the behavior.

        if os.getenv("SETUPTOOLS_USE_DISTUTILS") == "stdlib":
            # pytest.warns reset the warning filter temporarily
            # https://github.com/pytest-dev/pytest/issues/4011#issuecomment-423494810
            warnings.filterwarnings(
                "ignore",
                "'encoding' argument not specified",
                module="distutils.text_file",
                # This warning is already fixed in pypa/distutils but not in stdlib
            )

        build_py.finalize_options()
        build_py.run()

    build_dir = Path(dist.get_command_obj("build_py").build_lib)
    assert (build_dir / "mypkg/__init__.py").exists()
    assert (build_dir / "mypkg/resource_file.txt").exists()

    # Setuptools is configured to ignore `mypkg.tests`, therefore the following
    # files/dirs should not be included in the distribution.
    for f in [
        "mypkg/tests/__init__.py",
        "mypkg/tests/test_mypkg.py",
        "mypkg/tests/test_file.txt",
        "mypkg/tests",
    ]:
        with pytest.raises(AssertionError):
            # TODO: Enforce the following assertion once #3260 is fixed
            # (remove context manager and the following xfail).
            assert not (build_dir / f).exists()

    pytest.xfail("#3260")

