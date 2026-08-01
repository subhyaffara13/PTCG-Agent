
def dict_infer_unary_op(self, op):
    return _infer_unary_op(dict(self.items), op)

