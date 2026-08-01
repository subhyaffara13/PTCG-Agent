
def prim_min(g: jit_utils.GraphContext, self, other=None):
    if not other:
        if symbolic_helper._is_packed_list(self):
            self = stack(g, self, g.op("Constant", value_t=torch.tensor([0])))
        # pyrefly: ignore [no-matching-overload]
        return min(g, self)
    # pyrefly: ignore [no-matching-overload]
    return min(g, self, other)

