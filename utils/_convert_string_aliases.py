
def _convert_string_aliases(deriv, target_shape):
    if isinstance(deriv, str):
        if deriv == "clamped":
            deriv = [(1, np.zeros(target_shape))]
        elif deriv == "natural":
            deriv = [(2, np.zeros(target_shape))]
        else:
            raise ValueError(f"Unknown boundary condition : {deriv}")
    return deriv

