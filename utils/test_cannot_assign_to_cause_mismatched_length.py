
def test_cannot_assign_to_cause_mismatched_length():
    expr = (1, 2)
    assign_to = symbols('x y z')
    raises(ValueError, lambda: glsl_code(expr, assign_to))

