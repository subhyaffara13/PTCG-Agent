import math


def get_score(
    addr: sympy.Expr, var_ranges: dict[sympy.Symbol, int], buf_names: OrderedSet[str]
) -> int:
    """
    Score addr according to its approximate size.
    """
    # TODO - deduplicate with candidate_tilings
    var_sizes = []
    for v in addr.free_symbols:
        v_size = var_ranges.get(v)
        # TODO - reason about indirect vars
        if not symbol_is_type(v, SymT.INDIRECT) and v_size is not None:
            var_sizes.append(v_size)
    from .virtualized import V

    return V.graph.sizevars.optimization_hint(sympy_product(var_sizes))


def get_score(left_move, right_move):
    # This method exists in this file so it can be consumed from rps.py and agents.py without a circular dependency
    delta = right_move - left_move if (left_move + right_move) % 2 == 0 else left_move - right_move
    return 0 if delta == 0 else math.copysign(1, delta)

