
def _move_install_requirements_markers(
    install_requires: _StrOrIter, extras_require: Mapping[str, _Ordered[Requirement]]
) -> tuple[list[str], dict[str, list[str]]]:
    """
    The ``requires.txt`` file has an specific format:
        - Environment markers need to be part of the section headers and
          should not be part of the requirement spec itself.

    Move requirements in ``install_requires`` that are using environment
    markers ``extras_require``.
    """

    # divide the install_requires into two sets, simple ones still
    # handled by install_requires and more complex ones handled by extras_require.

    inst_reqs = list(_reqs.parse(install_requires))
    simple_reqs = filter(_no_marker, inst_reqs)
    complex_reqs = filterfalse(_no_marker, inst_reqs)
    simple_install_requires = list(map(str, simple_reqs))

    for r in complex_reqs:
        extras_require[':' + str(r.marker)].setdefault(r)

    expanded_extras = dict(
        # list(dict.fromkeys(...))  ensures a list of unique strings
        (k, list(dict.fromkeys(str(r) for r in map(_clean_req, v))))
        for k, v in extras_require.items()
    )

    return simple_install_requires, expanded_extras

