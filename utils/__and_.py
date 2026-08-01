
def __and_(g: jit_utils.GraphContext, self, other):
    # do type promotion (scalars don't seem to apply)
    args = [self, other]
    # type promotion doesn't happen with torch.bitwise_and(tensor, scalar)
    prom_args = [arg for arg in args if symbolic_helper._get_tensor_rank(arg)]
    if len(prom_args) == 0:
        prom_args = args
    promotion_jit_type = symbolic_helper._type_promote_from_values(*prom_args)
    self = symbolic_helper._maybe_cast_to_type(g, self, promotion_jit_type)
    other = symbolic_helper._maybe_cast_to_type(g, other, promotion_jit_type)
    if promotion_jit_type == _type_utils.JitScalarType.BOOL:
        return g.op("And", self, other)
    return g.op("BitwiseAnd", self, other)


def __and_(g: jit_utils.GraphContext, input, other):
    if not symbolic_helper._is_bool(input):
        raise errors.SymbolicValueError(
            "ONNX export does NOT support exporting bitwise AND "
            "for non-boolean input values",
            input,
        )
    if not symbolic_helper._is_bool(other):
        raise errors.SymbolicValueError(
            "ONNX export does NOT support exporting bitwise AND "
            "for non-boolean input values",
            other,
        )
    return g.op("And", input, other)

