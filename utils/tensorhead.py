
def tensorhead(name, typ, sym=None, comm=0):
    """
    Function generating tensorhead(s). This method is deprecated,
    use TensorHead constructor or tensor_heads() instead.

    Parameters
    ==========

    name : name or sequence of names (as in ``symbols``)

    typ :  index types

    sym :  same as ``*args`` in ``tensorsymmetry``

    comm : commutation group number
    see ``_TensorManager.set_comm``
    """
    if sym is None:
        sym = [[1] for i in range(len(typ))]
    with ignore_warnings(SymPyDeprecationWarning):
        sym = tensorsymmetry(*sym)
    return TensorHead(name, typ, sym, comm)

