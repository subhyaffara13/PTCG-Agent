
def test_jl_matrixsymbol_slice_autoname():
    A = MatrixSymbol('A', 2, 3)
    B = MatrixSymbol('B', 1, 3)
    name_expr = ("test", [Equality(B, A[0,:]), A[1,:], A[:,0], A[:,1]])
    result, = codegen(name_expr, "Julia", header=False, empty=False)
    source = result[1]
    expected = (
        "function test(A)\n"
        "    B = A[1,:]\n"
        "    out2 = A[2,:]\n"
        "    out3 = A[:,1]\n"
        "    out4 = A[:,2]\n"
        "    return B, out2, out3, out4\n"
        "end\n"
    )
    assert source == expected

