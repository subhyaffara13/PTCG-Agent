
def test_multiple_results_f():
    x, y, z = symbols('x,y,z')
    expr1 = (x + y)*z
    expr2 = (x - y)*z
    routine = make_routine(
        "test",
        [expr1, expr2]
    )
    code_gen = FCodeGen()
    raises(CodeGenError, lambda: get_string(code_gen.dump_h, [routine]))

