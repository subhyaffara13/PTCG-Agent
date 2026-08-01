
def _unflatten(input, proto):
    # unflatten a list or tuple input into a nested list/tuple structure
    # specified by proto
    def unflatten_helper(input, proto):
        res: list[torch.Tensor | None] = []
        if hasattr(proto, "_jit_wrap"):
            return proto._jit_wrap(input)
        if not isinstance(proto, (list, tuple)):
            return input[0], input[1:]
        for e in proto:
            if e is None:
                res.append(e)
            else:
                res_e, input = unflatten_helper(input, e)
                res.append(res_e)
        return type(proto)(res), input

    return unflatten_helper(input, proto)[0]

