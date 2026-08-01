
def tensor_product_simp_Pow(e):
    """Evaluates ``Pow`` expressions whose base is ``TensorProduct``

    .. deprecated:: 1.14.
        The transformations applied by this function are not done automatically
        when tensor products are combined.
    """
    sympy_deprecation_warning(
        """
        tensor_product_simp_Pow has been deprecated. The transformations
        performed by this function are now done automatically when
        tensor products are exponentiated.
        """,
        deprecated_since_version="1.14",
        active_deprecations_target='deprecated-tensorproduct-simp'
    )
    return e

