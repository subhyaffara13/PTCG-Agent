import sys

def patch_all() -> None:
    import setuptools

    # we can't patch distutils.cmd, alas
    distutils.core.Command = setuptools.Command  # type: ignore[misc,assignment] # monkeypatching

    _patch_distribution_metadata()

    # Install Distribution throughout the distutils
    for module in distutils.dist, distutils.core, distutils.cmd:
        module.Distribution = setuptools.dist.Distribution

    # Install the patched Extension
    distutils.core.Extension = setuptools.extension.Extension  # type: ignore[misc,assignment] # monkeypatching
    distutils.extension.Extension = setuptools.extension.Extension  # type: ignore[misc,assignment] # monkeypatching
    if 'distutils.command.build_ext' in sys.modules:
        sys.modules[
            'distutils.command.build_ext'
        ].Extension = setuptools.extension.Extension

