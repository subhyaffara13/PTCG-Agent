
def has_array_interface(array: ArrayType) -> ArrayType:
    if hasattr(array, "__array_interface__"):
        return True
    else:
        return False

