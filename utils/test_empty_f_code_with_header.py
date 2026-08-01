
def test_empty_f_code_with_header():
    code_gen = FCodeGen()
    source = get_string(code_gen.dump_f95, [], header=True)
    assert source[:82] == (
        "!******************************************************************************\n!*"
    )
          #   "                    Code generated with SymPy 0.7.2-git                    "
    assert source[158:] == (                                                              "*\n"
            "!*                                                                            *\n"
            "!*              See http://www.sympy.org/ for more information.               *\n"
            "!*                                                                            *\n"
            "!*                       This file is part of 'project'                       *\n"
            "!******************************************************************************\n"
            )

