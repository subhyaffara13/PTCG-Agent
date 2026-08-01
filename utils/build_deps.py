
def build_deps(package, sdist_file):
    """Find out what are the build dependencies for a package.

    "Manually" install them, since pip will not install build
    deps with `--no-build-isolation`.
    """
    # delay importing, since pytest discovery phase may hit this file from a
    # testenv without tomli
    from setuptools.compat.py310 import tomllib

    archive = Archive(sdist_file)
    info = tomllib.loads(_read_pyproject(archive))
    deps = info.get("build-system", {}).get("requires", [])
    deps += EXTRA_BUILD_DEPS.get(package, [])
    # Remove setuptools from requirements (and deduplicate)
    requirements = {Requirement(d).name: d for d in deps}
    return [v for k, v in requirements.items() if k != "setuptools"]

