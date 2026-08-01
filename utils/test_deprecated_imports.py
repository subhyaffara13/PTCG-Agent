
def test_deprecated_imports():
    x = symbols('x')

    with warns_deprecated_sympy():
        from sympy.core.basic import preorder_traversal
        preorder_traversal(x)
    with warns_deprecated_sympy():
        from sympy.simplify.simplify import bottom_up
        bottom_up(x, lambda x: x)
    with warns_deprecated_sympy():
        from sympy.simplify.simplify import walk
        walk(x, lambda x: x)
    with warns_deprecated_sympy():
        from sympy.simplify.traversaltools import use
        use(x, lambda x: x)
    with warns_deprecated_sympy():
        from sympy.utilities.iterables import postorder_traversal
        postorder_traversal(x)
    with warns_deprecated_sympy():
        from sympy.utilities.iterables import interactive_traversal
        capture(lambda: interactive_traversal(x))

