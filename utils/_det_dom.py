
def _det_DOM(M):
    DOM = DomainMatrix.from_Matrix(M, field=True, extension=True)
    K = DOM.domain
    return K.to_sympy(DOM.det())

