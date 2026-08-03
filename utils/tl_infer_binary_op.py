import itertools

def tl_infer_binary_op(
    self: _TupleListNodeT,
    opnode: nodes.AugAssign | nodes.BinOp,
    operator: str,
    other: InferenceResult,
    context: InferenceContext,
    method: SuccessfulInferenceResult,
) -> Generator[_TupleListNodeT | nodes.Const | util.UninferableBase]:
    """Infer a binary operation on a tuple or list.

    The instance on which the binary operation is performed is a tuple
    or list. This refers to the left-hand side of the operation, so:
    'tuple() + 1' or '[] + A()'
    """
    from astroid import helpers  # pylint: disable=import-outside-toplevel

    # For tuples and list the boundnode is no longer the tuple or list instance
    context.boundnode = None
    not_implemented = nodes.Const(NotImplemented)
    if isinstance(other, self.__class__) and operator == "+":
        node = self.__class__(parent=opnode)
        node.elts = list(
            itertools.chain(
                _filter_uninferable_nodes(self.elts, context),
                _filter_uninferable_nodes(other.elts, context),
            )
        )
        yield node
    elif isinstance(other, nodes.Const) and operator == "*":
        if not isinstance(other.value, int):
            yield not_implemented
            return
        yield _multiply_seq_by_int(self, opnode, other.value, context)
    elif isinstance(other, bases.Instance) and operator == "*":
        # Verify if the instance supports __index__.
        as_index = helpers.class_instance_as_index(other)
        if not as_index:
            yield util.Uninferable
        elif not isinstance(as_index.value, int):  # pragma: no cover
            # already checked by class_instance_as_index() but faster than casting
            raise AssertionError("Please open a bug report.")
        else:
            yield _multiply_seq_by_int(self, opnode, as_index.value, context)
    else:
        yield not_implemented

