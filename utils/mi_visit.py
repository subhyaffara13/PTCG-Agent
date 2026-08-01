
def mi_visit(code, multi):
    '''Visit the code and compute the Maintainability Index (MI) from it.'''
    return mi_compute(*mi_parameters(code, multi))

