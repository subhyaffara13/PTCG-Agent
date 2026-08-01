
def get_attr_inference_rule(n: Node, traced):
    """
    The current getattr rule only handles the shape attribute
    Can be extended to other attributes
    The most representative type we have is "Dyn" but the system
    can be extended with more types, such as a type to represent shapes
    """
    attr_name = n.args[1]

    if attr_name == "shape":
        n.type = Dyn
    else:
        raise TypeError("Not yet implemented")

    # TODO. We leave it like this till we add a type to represent tensor sizes
    return n.type


def get_attr_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    """
    If the attribute is "device" then the tensor shape is preserved
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    if not isinstance(n.args[1], str):
        raise AssertionError(f"Expected str, got {type(n.args[1])}")
    output, counter = gen_tvar(counter)
    symbols[n] = output

    input = symbols[n.args[0]]
    attr = n.args[1]

    if attr == "device":
        return [BinConstraintT(input, output, op_eq)], counter
    else:
        raise NotImplementedError("Not yet implemented")

