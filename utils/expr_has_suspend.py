
def expr_has_suspend(expr: Expression) -> bool:
    """Does evaluating 'expr' involve a suspension point (await/yield/yield from)?

    A whole-expression borrow can't safely span a suspension point, since the
    borrowed value and its borrow root are held in registers that aren't spilled
    into the generator environment across the suspend.
    """
    detector = SuspendDetector()
    expr.accept(detector)
    return detector.found

