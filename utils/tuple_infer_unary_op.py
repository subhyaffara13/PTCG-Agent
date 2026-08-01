
def tuple_infer_unary_op(self, op):
    return _infer_unary_op(tuple(self.elts), op)

