
def flex_name(op_id, dim):
    # Return the local variable name for the computed flexible size
    # for a given op and dimension.
    return f"s_{op_id}_{dim}"

