
def extras_from_dep(dep):
    try:
        markers = packaging.requirements.Requirement(dep).marker._markers
    except AttributeError:
        markers = ()
    return set(
        marker[2].value
        for marker in markers
        if isinstance(marker, tuple) and marker[0].value == 'extra'
    )

