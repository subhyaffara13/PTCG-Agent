
def _postprocess_tp_pow(expr):
    """Handle TensorProduct(*operators)**(positive integer).

    This handles a tensor product of operators, to an integer power.
    The power here is interpreted as regular multiplication, not
    tensor product exponentiation. The form of exponentiation performed
    here leaves the space and dimension of the object the same.

    This operation does not make sense for tensor product's of states.
    """
    base, exp = expr.as_base_exp()
    debug('_postprocess_tp_pow: ', base, exp, expr.args)
    if isinstance(base, TensorProduct) and exp.is_integer and exp.is_positive and base.kind == OperatorKind:
        new_args = [a**exp for a in base.args]
        return TensorProduct(*new_args)

