
def _array_equivalent_float(left: np.ndarray, right: np.ndarray) -> bool:
    return bool(((left == right) | (np.isnan(left) & np.isnan(right))).all())

