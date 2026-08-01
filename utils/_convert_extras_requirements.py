
def _convert_extras_requirements(
    extras_require: Mapping[str, _StrOrIter],
) -> defaultdict[str, _Ordered[Requirement]]:
    """
    Convert requirements in `extras_require` of the form
    `"extra": ["barbazquux; {marker}"]` to
    `"extra:{marker}": ["barbazquux"]`.
    """
    output = defaultdict[str, _Ordered[Requirement]](dict)
    for section, v in extras_require.items():
        # Do not strip empty sections.
        output[section]
        for r in _reqs.parse(v):
            output[section + _suffix_for(r)].setdefault(r)

    return output

