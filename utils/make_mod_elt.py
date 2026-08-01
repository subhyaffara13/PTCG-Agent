
def make_mod_elt(module, col, denom=1):
    r"""
    Factory function which builds a :py:class:`~.ModuleElement`, but ensures
    that it is a :py:class:`~.PowerBasisElement` if the module is a
    :py:class:`~.PowerBasis`.
    """
    if isinstance(module, PowerBasis):
        return PowerBasisElement(module, col, denom=denom)
    else:
        return ModuleElement(module, col, denom=denom)

