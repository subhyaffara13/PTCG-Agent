
def get_postprocessor(cls):
    def _postprocessor(expr):
        tens_class = {Mul: TensMul, Add: TensAdd}[cls]
        if any(isinstance(a, TensExpr) for a in expr.args):
            return tens_class(*expr.args)
        else:
            return expr

    return _postprocessor


def get_postprocessor(cls):
    def _postprocessor(expr):
        vec_class = {Add: VectorAdd}[cls]
        vectors = []
        for term in expr.args:
            if isinstance(term.kind, VectorKind):
                vectors.append(term)

        if vec_class == VectorAdd:
            return VectorAdd(*vectors).doit(deep=False)
    return _postprocessor


def get_postprocessor(cls):
    def _postprocessor(expr):
        # To avoid circular imports, we can't have MatMul/MatAdd on the top level
        mat_class = {Mul: MatMul, Add: MatAdd}[cls]
        nonmatrices = []
        matrices = []
        for term in expr.args:
            if isinstance(term, MatrixExpr):
                matrices.append(term)
            else:
                nonmatrices.append(term)

        if not matrices:
            return cls._from_args(nonmatrices)

        if nonmatrices:
            if cls == Mul:
                for i in range(len(matrices)):
                    if not matrices[i].is_MatrixExpr:
                        # If one of the matrices explicit, absorb the scalar into it
                        # (doit will combine all explicit matrices into one, so it
                        # doesn't matter which)
                        matrices[i] = matrices[i].__mul__(cls._from_args(nonmatrices))
                        nonmatrices = []
                        break

            else:
                # Maintain the ability to create Add(scalar, matrix) without
                # raising an exception. That way different algorithms can
                # replace matrix expressions with non-commutative symbols to
                # manipulate them like non-commutative scalars.
                return cls._from_args(nonmatrices + [mat_class(*matrices).doit(deep=False)])

        if mat_class == MatAdd:
            return mat_class(*matrices).doit(deep=False)
        return mat_class(cls._from_args(nonmatrices), *matrices).doit(deep=False)
    return _postprocessor

