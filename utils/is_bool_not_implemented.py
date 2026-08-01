
def is_bool_not_implemented(data, op_name):
    # match non-masked behavior
    return data.dtype.kind == "b" and op_name.strip("_").lstrip("r") in [
        "pow",
        "truediv",
        "floordiv",
    ]

