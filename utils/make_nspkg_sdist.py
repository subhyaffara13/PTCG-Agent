
def make_nspkg_sdist(dist_path, distname, version):
    """
    Make an sdist tarball with distname and version which also contains one
    package with the same name as distname.  The top-level package is
    designated a namespace package).
    """
    # Assert that the distname contains at least one period
    assert '.' in distname

    parts = distname.split('.')
    nspackage = parts[0]

    packages = ['.'.join(parts[:idx]) for idx in range(1, len(parts) + 1)]

    setup_py = DALS(
        f"""\
        import setuptools
        setuptools.setup(
            name={distname!r},
            version={version!r},
            packages={packages!r},
            namespace_packages=[{nspackage!r}]
        )
    """
    )

    init = "__import__('pkg_resources').declare_namespace(__name__)"

    files = [('setup.py', setup_py), (os.path.join(nspackage, '__init__.py'), init)]
    for package in packages[1:]:
        filename = os.path.join(*(package.split('.') + ['__init__.py']))
        files.append((filename, ''))

    make_sdist(dist_path, files)

