
def __not_(g: jit_utils.GraphContext, self):
    if not symbolic_helper._is_bool(self):
        raise errors.SymbolicValueError(
            "ONNX export does NOT support exporting bitwise Not "
            "for non-boolean input values",
            self,
        )
    return g.op("Not", self)

