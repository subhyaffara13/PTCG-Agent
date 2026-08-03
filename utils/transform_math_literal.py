import math


def transform_math_literal(builder: IRBuilder, fullname: str, line: int) -> Value | None:
    if fullname == "math.e":
        return builder.load_float(math.e, line)
    if fullname == "math.pi":
        return builder.load_float(math.pi, line)
    if fullname == "math.inf":
        return builder.load_float(math.inf, line)
    if fullname == "math.nan":
        return builder.load_float(math.nan, line)
    if fullname == "math.tau":
        return builder.load_float(math.tau, line)

    return None

