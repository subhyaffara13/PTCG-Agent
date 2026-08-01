
def prim_dtype(g: jit_utils.GraphContext, self):
    scalar_type = symbolic_helper._try_get_scalar_type(self)
    if scalar_type is None:
        scalar_type = _type_utils.JitScalarType.FLOAT
    # This node records a torch dtype as int
    return g.op("Constant", value_t=torch.tensor(scalar_type))

