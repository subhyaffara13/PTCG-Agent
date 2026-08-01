
def _simplify_loads(loads):
    return [
        load.__class__(load.location, load.vector.simplify())
        for load in loads
    ]

