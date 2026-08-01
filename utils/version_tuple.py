
def version_tuple(vstring):
    # Parse a version string to a tuple e.g. '1.2' -> (1, 2)
    # Simplified from distutils.version.LooseVersion which was deprecated in
    # Python 3.10.
    components = []
    for x in _component_re.split(vstring):
        if x and x != '.':
            try:
                x = int(x)
            except ValueError:
                pass
            components.append(x)
    return tuple(components)

