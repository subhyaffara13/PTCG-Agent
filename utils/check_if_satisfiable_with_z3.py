
def check_if_satisfiable_with_z3(constraints):
    from sympy.external.importtools import import_module
    from sympy.printing.smtlib import smtlib_code
    from sympy.logic.boolalg import And
    boolean_formula = And(*constraints)
    z3 = import_module("z3")
    if z3:
        smtlib_string = smtlib_code(boolean_formula)
        s = z3.Solver()
        s.from_string(smtlib_string)
        res = str(s.check())
        if res == 'sat':
            return True
        elif res == 'unsat':
            return False
        else:
            raise ValueError(f"z3 was not able to check the satisfiability of {boolean_formula}")

