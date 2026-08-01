
def test_print_tree_MatAdd_noassumptions():
    from sympy.matrices.expressions import MatrixSymbol
    A = MatrixSymbol('A', 3, 3)
    B = MatrixSymbol('B', 3, 3)

    test_str = \
"""MatAdd: A + B
+-MatrixSymbol: A
| +-Str: A
| +-Integer: 3
| +-Integer: 3
+-MatrixSymbol: B
  +-Str: B
  +-Integer: 3
  +-Integer: 3
"""

    assert tree(A + B, assumptions=False) == test_str

