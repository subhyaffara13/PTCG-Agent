
def raise_for_nan(value: object, method: str) -> None:
    if lib.is_float(value) and np.isnan(value):
        raise ValueError(f"Cannot perform logical '{method}' with floating NaN")

