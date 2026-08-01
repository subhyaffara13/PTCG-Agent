
def make_python_requires_sdist(dist_path, distname, version, python_requires):
    make_sdist(
        dist_path,
        [
            (
                'setup.py',
                DALS(
                    """\
                import setuptools
                setuptools.setup(
                  name={name!r},
                  version={version!r},
                  python_requires={python_requires!r},
                )
                """
                ).format(
                    name=distname, version=version, python_requires=python_requires
                ),
            ),
            ('setup.cfg', ''),
        ],
    )

