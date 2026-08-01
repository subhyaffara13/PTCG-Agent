
def _fetch_build_eggs(dist, requires: _reqs._StrOrIter) -> list[metadata.Distribution]:
    _DeprecatedInstaller.emit(stacklevel=3)
    _warn_wheel_not_available(dist)

    parsed_reqs = _reqs.parse(requires)

    missing_reqs = itertools.filterfalse(_present, parsed_reqs)

    needed_reqs = (
        req for req in missing_reqs if not req.marker or req.marker.evaluate()
    )
    resolved_dists = [_fetch_build_egg_no_warn(dist, req) for req in needed_reqs]
    for dist in resolved_dists:
        # dist.locate_file('') is the directory containing EGG-INFO, where the importabl
        # contents can be found.
        sys.path.insert(0, str(dist.locate_file('')))
    return resolved_dists


def _fetch_build_eggs(dist: Distribution):
    try:
        dist.fetch_build_eggs(dist.setup_requires)
    except Exception as ex:
        msg = """
        It is possible a package already installed in your system
        contains an version that is invalid according to PEP 440.
        You can try `pip install --use-pep517` as a workaround for this problem,
        or rely on a new virtual environment.

        If the problem refers to a package that is not installed yet,
        please contact that package's maintainers or distributors.
        """
        if "InvalidVersion" in ex.__class__.__name__:
            if hasattr(ex, "add_note"):
                ex.add_note(msg)  # PEP 678
            else:
                dist.announce(f"\n{msg}\n")
        raise

