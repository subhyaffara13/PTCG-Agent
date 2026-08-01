
def _parse_output_order(order, a_is_fcontig, b_is_fcontig):
    order = order.upper()
    if order == "K":
        return None
    elif order in "CF":
        return order
    elif order == "A":
        if a_is_fcontig and b_is_fcontig:
            return "F"
        else:
            return "C"
    else:
        raise ValueError(
            "ValueError: order must be one of "
            f"'C', 'F', 'A', or 'K' (got '{order}')"
        )

