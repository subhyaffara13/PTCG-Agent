
def get_triton_reduction_function(reduction_type):
    use_helper = reduction_type in ("any", "max", "min", "prod")
    module = "triton_helpers" if use_helper else "tl"
    if reduction_type in ("max", "min"):
        return f"{module}.{reduction_type}2"
    else:
        return f"{module}.{reduction_type}"

