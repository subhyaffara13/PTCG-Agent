
def subscript_chain_is_equal(left: nodes.Subscript, right: nodes.Subscript) -> bool:
    while isinstance(left, nodes.Subscript) and isinstance(right, nodes.Subscript):
        try:
            if (
                get_subscript_const_value(left).value
                != get_subscript_const_value(right).value
            ):
                return False

            left = left.value
            right = right.value
        except InferredTypeError:
            return False

    return left.as_string() == right.as_string()  # type: ignore[no-any-return]

