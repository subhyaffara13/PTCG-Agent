
def tensor_product_simp(e, **hints):
    """Try to simplify and combine tensor products.

    .. deprecated:: 1.14.
        The transformations applied by this function are not done automatically
        when tensor products are combined.

    Originally, this function tried to pull expressions inside of ``TensorProducts``.
    It only worked for relatively simple cases where the products have
    only scalars, raw ``TensorProducts``, not ``Add``, ``Pow``, ``Commutators``
    of ``TensorProducts``.
    """
    sympy_deprecation_warning(
        """
        tensor_product_simp has been deprecated. The transformations
        performed by this function are now done automatically when
        tensor products are combined.
        """,
        deprecated_since_version="1.14",
        active_deprecations_target='deprecated-tensorproduct-simp'
    )
    return e

