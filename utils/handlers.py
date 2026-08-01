
def handlers():
    # TODO add CeilDiv (it doesn't appear in the index_expr)

    # TODO default to some decompositions if the interpreter doesn't have them
    # like decomposing ModularIndexing or implementing Le(a,b) as Ge(b, a)

    HANDLERS = {
        sympy.Or: "or_",
        sympy.And: "and_",
        sympy.Eq: "eq",
        sympy.Ne: "ne",
        sympy.Lt: "lt",
        sympy.Gt: "gt",
        sympy.Le: "le",
        sympy.Ge: "ge",
        sympy.Not: "not_",
        IntTrueDiv: "int_truediv",
        FloatTrueDiv: "truediv",
        FloorDiv: "floordiv",
        CleanDiv: "floordiv",  # TODO: hmm?
        TruncToFloat: "trunc",
        Where: "where",
        sympy.Add: "add",
        sympy.Mul: "mul",
        FloatPow: "pow",
        PowByNatural: "pow_by_natural",
        # sympy simplifies x * x into Pow(x, 2), so we need to handle this.
        # Do NOT use builtin Pow for floats
        # TODO: There is a hazard here, if we have float * float it will
        # also get turned into Pow(float, 2) but we don't want this because
        # pow_by_natural is assumed to only be integers.  Probably the fix is
        # to add a FloatMul to impede this optimization
        sympy.Pow: "pow_by_natural",
        Mod: "mod",
        PythonMod: "python_mod",
        # TODO: Inductor can generate these, but it's ill-specified which
        # semantics were intended here.  Needs to be cleaned up along with
        # FloorDiv in a bigger cleanup
        sympy.Mod: "mod",
        sympy.Abs: "abs",
        sympy.log: "log",
        sympy.exp: "exp",
        sympy.Min: "minimum",
        sympy.Max: "maximum",
        Min: "minimum",
        Max: "maximum",
        ModularIndexing: "modular_indexing",
        sympy.functions.elementary.piecewise.ExprCondPair: "expr_cond_pair",
        sympy.Piecewise: "piecewise",
        Identity: "identity",
        IsNonOverlappingAndDenseIndicator: "is_non_overlapping_and_dense_indicator",
        RoundDecimal: "round_decimal",
        # TODO: do the rest of the opaque unary functions...
        OpaqueUnaryFn_log2: "log2",
        BitwiseFn_bitwise_and: "bitwise_and",
        BitwiseFn_bitwise_or: "bitwise_or",
        BitwiseFn_bitwise_xor: "bitwise_xor",
    }
    # TODO: This is kind of pointless, we shouldn't be generating sympy.sin
    # for these functions, they should be Opaque instead
    for name in ["cos", "sin", "tan", "sinh", "cosh", "tanh", "asin", "acos", "atan"]:
        HANDLERS[getattr(sympy, name)] = name

    return HANDLERS

