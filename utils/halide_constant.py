
def halide_constant(val):
    if isinstance(val, int) and not (-2147483648 <= val <= 2147483647):
        info = torch.iinfo(torch.int64)
        if val == info.min:
            return "hl.Int(64).min()"
        if val == info.max:
            return "hl.Int(64).max()"
        return f"hl.i64({val!r})"
    if isinstance(val, float):
        return f"hl.f64({constant_repr(val)})"
    return repr(val)

