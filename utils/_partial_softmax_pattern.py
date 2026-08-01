
def _partial_softmax_pattern(linear_func, reverse=False, to_dtype=False):
    # Allow matching inp * other and other * input
    if reverse:
        scaled = CallFunction(
            linear_func, KeywordArg("other"), KeywordArg("inp"), _users=MULTIPLE
        )
    else:
        scaled = CallFunction(
            linear_func, KeywordArg("inp"), KeywordArg("other"), _users=MULTIPLE
        )
    if to_dtype:
        scaled = CallFunction(
            prims.convert_element_type, scaled, KeywordArg("dtype"), _users=MULTIPLE
        )
    amax = CallFunction(
        aten.amax.default, scaled, KeywordArg("dim"), KeywordArg("keepdim")
    )
    return CallFunction(aten.sub.Tensor, scaled, amax)

