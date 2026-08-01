
def vec_items(builder: LowLevelIRBuilder, vecobj: Value) -> Value:
    """Return pointer to first item in vec.

    The items field points directly to the first element in the buffer.
    """
    return builder.get_element(vecobj, "items")

