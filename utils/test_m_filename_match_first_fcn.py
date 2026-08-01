
def test_m_filename_match_first_fcn():
    name_expr = [ ("foo", [2*x, 3*y]), ("bar", [y**2, 4*y]) ]
    raises(ValueError, lambda: codegen(name_expr,
                        "Octave", prefix="bar", header=False, empty=False))

