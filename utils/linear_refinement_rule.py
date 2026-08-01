
def linear_refinement_rule(n: Node):
    """
    The equality constraints are between the first dimension of
    the input and output
    """
    res = []
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    arg_type = n.args[0].type
    if isinstance(arg_type, TensorType) and isinstance(n.type, TensorType):
        res = [Equality(arg_type.__args__[0], n.type.__args__[0])]
    return res

