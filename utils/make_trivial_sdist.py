
def make_trivial_sdist(dist_path, distname, version, setuptools_wheel=None):
    """
    Create a simple sdist tarball at dist_path, containing just a simple
    setup.py.

    If ``setuptools_wheel`` is passed, a ``pyproject.toml`` file will also
    be generated and the passed value will be used as location for
    setuptools (as build dependency).
    """
    files = [
        (
            'setup.py',
            DALS(
                f"""\
                 import setuptools
                 setuptools.setup(
                     name={distname!r},
                     version={version!r}
                 )
                 """
            ),
        ),
        ('setup.cfg', ''),
    ]

    if setuptools_wheel:
        files.append((
            "pyproject.toml",
            DALS(
                f"""\
                [build-system]
                requires = ["setuptools @ {setuptools_wheel.as_uri()}"]
                build-backend = "setuptools.build_meta"
                """
            ),
        ))

    make_sdist(dist_path, files)

