
def assert_simplify_expand(e1, e2):
    """Helper for simplifying and expanding results.

    This is needed to help us test complex expressions whose form
    might change in subtle ways as the rest of sympy evolves.
    """
    assert simplify(e1.expand(tensorproduct=True)) == \
        simplify(e2.expand(tensorproduct=True))

