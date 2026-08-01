
def variance_string(variance: int) -> str:
    if variance == COVARIANT:
        return "covariant"
    elif variance == CONTRAVARIANT:
        return "contravariant"
    else:
        return "invariant"

