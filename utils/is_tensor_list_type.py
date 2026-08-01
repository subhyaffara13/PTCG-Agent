
def is_tensor_list_type(t: Type) -> bool:
    # TODO: Should handle optional here?
    return t.is_tensor_like() and t.is_list_like() is not None

