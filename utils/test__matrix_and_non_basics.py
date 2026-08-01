
def test_Matrix_and_non_basics():
    from sympy.matrices.expressions.matexpr import MatrixSymbol
    n = Symbol('n')
    assert dotprint(MatrixSymbol('X', n, n)) == \
"""digraph{

# Graph style
"ordering"="out"
"rankdir"="TD"

#########
# Nodes #
#########

"MatrixSymbol(Str('X'), Symbol('n'), Symbol('n'))_()" ["color"="black", "label"="MatrixSymbol", "shape"="ellipse"];
"Str('X')_(0,)" ["color"="blue", "label"="X", "shape"="ellipse"];
"Symbol('n')_(1,)" ["color"="black", "label"="n", "shape"="ellipse"];
"Symbol('n')_(2,)" ["color"="black", "label"="n", "shape"="ellipse"];

#########
# Edges #
#########

"MatrixSymbol(Str('X'), Symbol('n'), Symbol('n'))_()" -> "Str('X')_(0,)";
"MatrixSymbol(Str('X'), Symbol('n'), Symbol('n'))_()" -> "Symbol('n')_(1,)";
"MatrixSymbol(Str('X'), Symbol('n'), Symbol('n'))_()" -> "Symbol('n')_(2,)";
}"""

