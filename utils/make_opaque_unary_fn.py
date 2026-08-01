
def make_opaque_unary_fn(name):
    class OpaqueUnaryFn(sympy.Function):
        """
        Unlike the builtin sympy functions on real numbers like sympy.sqrt,
        these equivalents do not do any nontrivial reasoning besides
        constant propagation.  This helps avoid performing transformations
        that are valid for real numbers but are invalid for floating point;
        in particular, while we are willing to make optimizations that change
        numerics for Tensor compute, we are NOT willing to make optimizations
        that change numerics for size compute.
        """

        _torch_handler_name = name
        _torch_unpickler = make_opaque_unary_fn

        @classmethod
        def eval(cls, a):
            if isinstance(a, (sympy.Integer, sympy.Float)):
                # Python converts to float64 before computing, c.f.
                # >>> math.sin(2**53+1)
                # -0.848925964814655
                # >>> math.sin(float(2**53+1))
                # -0.848925964814655
                try:
                    return sympy.Float(getattr(math, name)(float(a)))
                # Just use sympy semantics for infinity/overflow, you might get some
                # weird objects but ask silly questions, get silly answers
                except OverflowError:
                    return getattr(sympy, name)(a)
            elif a in [sympy.oo, -sympy.oo, sympy.zoo, -sympy.zoo, int_oo, -int_oo]:
                if a is int_oo:
                    a = sympy.oo
                if a is -int_oo:
                    a = -sympy.oo
                if name == "log2":
                    return sympy.log(a, 2)
                return getattr(sympy, name)(a)
            return None

    nm = "OpaqueUnaryFn_" + name
    OpaqueUnaryFn.__name__ = nm
    OpaqueUnaryFn.__qualname__ = nm

    return OpaqueUnaryFn

