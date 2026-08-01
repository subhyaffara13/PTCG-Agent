
def test_multiple_results_c():
    x, y, z = symbols('x,y,z')
    expr1 = (x + y)*z
    expr2 = (x - y)*z
    routine = make_routine(
        "test",
        [expr1, expr2]
    )
    code_gen = C99CodeGen()
    raises(CodeGenError, lambda: get_string(code_gen.dump_h, [routine]))

