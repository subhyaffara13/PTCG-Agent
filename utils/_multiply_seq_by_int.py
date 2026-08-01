
def _multiply_seq_by_int(
    self: _TupleListNodeT,
    opnode: nodes.AugAssign | nodes.BinOp,
    value: int,
    context: InferenceContext,
) -> _TupleListNodeT:
    node = self.__class__(parent=opnode)
    if not (value > 0 and self.elts):
        node.elts = []
        return node
    if len(self.elts) * value > 1e8:
        node.elts = [util.Uninferable]
        return node
    filtered_elts = (
        util.safe_infer(elt, context) or util.Uninferable
        for elt in self.elts
        if not isinstance(elt, util.UninferableBase)
    )
    node.elts = list(filtered_elts) * value
    return node

