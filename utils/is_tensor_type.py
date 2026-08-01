
def is_tensor_type(t: Type) -> bool:
    # TODO: Should handle optional here?
    return t.is_tensor_like() and t.is_list_like() is None

