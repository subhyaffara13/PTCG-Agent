
def test_empty_c_code_with_comment():
    code_gen = C89CodeGen()
    source = get_string(code_gen.dump_c, [], header=True)
    assert source[:82] == (
        "/******************************************************************************\n *"
    )
          #   "                    Code generated with SymPy 0.7.2-git                    "
    assert source[158:] == (                                                              "*\n"
            " *                                                                            *\n"
            " *              See http://www.sympy.org/ for more information.               *\n"
            " *                                                                            *\n"
            " *                       This file is part of 'project'                       *\n"
            " ******************************************************************************/\n"
            "#include \"file.h\"\n"
            "#include <math.h>\n"
            )

