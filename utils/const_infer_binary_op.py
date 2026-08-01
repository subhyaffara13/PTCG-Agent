
def const_infer_binary_op(
    self: nodes.Const,
    opnode: nodes.AugAssign | nodes.BinOp,
    operator: str,
    other: InferenceResult,
    context: InferenceContext,
    _: SuccessfulInferenceResult,
) -> Generator[ConstFactoryResult | util.UninferableBase]:
    not_implemented = nodes.Const(NotImplemented)
    if isinstance(other, nodes.Const):
        if (
            operator == "**"
            and isinstance(self.value, (int, float))
            and isinstance(other.value, (int, float))
            and (self.value > 1e5 or other.value > 1e5)
        ):
            yield not_implemented
            return
        try:
            impl = BIN_OP_IMPL[operator]
            try:
                yield nodes.const_factory(impl(self.value, other.value))
            except TypeError:
                # ArithmeticError is not enough: float >> float is a TypeError
                yield not_implemented
            except Exception:  # pylint: disable=broad-except
                yield util.Uninferable
        except TypeError:
            yield not_implemented
    elif isinstance(self.value, str) and operator == "%":
        # TODO(cpopa): implement string interpolation later on.
        yield util.Uninferable
    else:
        yield not_implemented

