
def tensor_product_simp_Mul(e):
    """Simplify a Mul with tensor products.

    .. deprecated:: 1.14.
        The transformations applied by this function are not done automatically
        when tensor products are combined.

    Originally, the main use of this function is to simplify a ``Mul`` of
    ``TensorProduct``s to a ``TensorProduct`` of ``Muls``.
    """
    sympy_deprecation_warning(
        """
        tensor_product_simp_Mul has been deprecated. The transformations
        performed by this function are now done automatically when
        tensor products are multiplied.
        """,
        deprecated_since_version="1.14",
        active_deprecations_target='deprecated-tensorproduct-simp'
    )
    return e

