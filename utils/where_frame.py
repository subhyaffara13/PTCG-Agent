
def where_frame(request, float_string_frame, mixed_float_frame, mixed_int_frame):
    if request.param == "default":
        return DataFrame(
            np.random.default_rng(2).standard_normal((5, 3)), columns=["A", "B", "C"]
        )
    if request.param == "float_string":
        return float_string_frame
    if request.param == "mixed_float":
        return mixed_float_frame
    if request.param == "mixed_int":
        return mixed_int_frame

