
def reshape_inference_rule(n: Node):
    """
    Without dynamism, the rule checks that the
    product of the elements of the argument tensor
    type is equal to the product of the elements
    of the required shape. We gradualize this rule
    by adding a case to handle fully dynamic input
    as well as input where some of the tensor dimensions
    are unknown. In this case we check for divisibility
    """
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")
    t1 = n.args[0].type

    if not isinstance(n.args[1], list):
        raise AssertionError(f"Expected list, got {type(n.args[1])}")
    t2 = n.args[1]
    t2_type = TensorType([Dyn if elem == -1 else elem for elem in t2])

    # if we do not know the original tensor dimension,
    # we return the required dimension
    if t1 == Dyn:
        n.type = t2_type
        return t2_type

    # if any of the dimensions are unknown,
    # we check for divisibility
    elif isinstance(t1, TensorType):
        if not isinstance(t1, TensorType):
            raise AssertionError(f"Expected TensorType, got {type(t1)}")
        a = [e if e != Dyn else 1 for e in t1.__args__]
        p1 = reduce(operator.mul, a)
        p2 = reduce(operator.mul, t2)
        if p1 % p2 == 0 or p2 % p1 == 0:
            n.type = t2_type
            return t2_type
        else:
            raise TypeError(f"Cannot reshape in node {n} from {t1} to {t2_type}")
    else:
        raise TypeError(f"Cannot reshape in node {n} from {t1} to {t2_type}")


def reshape_inference_rule(
    n: Node, symbols: _SymbolDict, constraints: list[Constraint], counter: int
) -> tuple[list[Constraint], int]:
    if not isinstance(n.args[0], Node):
        raise AssertionError(f"Expected Node, got {type(n.args[0])}")

    # generate the new variable
    my_reshape, counter = gen_tvar(counter)
    symbols[n] = my_reshape

    src_var = symbols[n.args[0]]
    t2 = n.args[1]
    t2_type = TensorType([Dyn if elem == -1 else elem for elem in t2])  # type: ignore[union-attr]
    c1 = BinConstraintT(my_reshape, t2_type, op_eq)  # type: ignore[union-attr]
    c2 = CanReshape(src_var, t2_type)  # pyrefly: ignore[bad-argument-type]

    return [c1, c2], counter

