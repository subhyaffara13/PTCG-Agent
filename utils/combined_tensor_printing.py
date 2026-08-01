
def combined_tensor_printing(combined):
    """Set flag controlling whether tensor products of states should be
    printed as a combined bra/ket or as an explicit tensor product of different
    bra/kets. This is a global setting for all TensorProduct class instances.

    Parameters
    ----------
    combine : bool
        When true, tensor product states are combined into one ket/bra, and
        when false explicit tensor product notation is used between each
        ket/bra.
    """
    global _combined_printing
    _combined_printing = combined

