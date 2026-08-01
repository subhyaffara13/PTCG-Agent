
def test_tensor_product_simp():
    with warns_deprecated_sympy():
        assert tensor_product_simp(TP(A, B)*TP(B, C)) == TP(A*B, B*C)
        # tests for Pow-expressions
        assert TP(A, B)**y == TP(A**y, B**y)
        assert tensor_product_simp(TP(A, B)**y) == TP(A**y, B**y)
        assert tensor_product_simp(x*TP(A, B)**2) == x*TP(A**2,B**2)
        assert tensor_product_simp(x*(TP(A, B)**2)*TP(C,D)) == x*TP(A**2*C,B**2*D)
        assert tensor_product_simp(TP(A,B)-TP(C,D)**y) == TP(A,B)-TP(C**y,D**y)

