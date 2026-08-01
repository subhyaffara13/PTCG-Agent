
def _a2m_mul(*args):
    if not any(isinstance(i, _CodegenArrayAbstract) for i in args):
        from sympy.matrices.expressions.matmul import MatMul
        return MatMul(*args).doit()
    else:
        return _array_contraction(
            _array_tensor_product(*args),
            *[(2*i-1, 2*i) for i in range(1, len(args))]
        )

