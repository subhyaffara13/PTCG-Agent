
def test_matrix_deprecated_isinstance():

    # Test that e.g. isinstance(M, MatrixCommon) still gives True when M is a
    # Matrix for each of the deprecated matrix classes.

    from sympy.matrices.common import (
        MatrixRequired,
        MatrixShaping,
        MatrixSpecial,
        MatrixProperties,
        MatrixOperations,
        MatrixArithmetic,
        MatrixCommon
    )
    from sympy.matrices.matrices import (
        MatrixDeterminant,
        MatrixReductions,
        MatrixSubspaces,
        MatrixEigen,
        MatrixCalculus,
        MatrixDeprecated
    )
    from sympy import (
        Matrix,
        ImmutableMatrix,
        SparseMatrix,
        ImmutableSparseMatrix
    )
    all_mixins = (
        MatrixRequired,
        MatrixShaping,
        MatrixSpecial,
        MatrixProperties,
        MatrixOperations,
        MatrixArithmetic,
        MatrixCommon,
        MatrixDeterminant,
        MatrixReductions,
        MatrixSubspaces,
        MatrixEigen,
        MatrixCalculus,
        MatrixDeprecated
    )
    all_matrices = (
        Matrix,
        ImmutableMatrix,
        SparseMatrix,
        ImmutableSparseMatrix
    )

    Ms = [M([[1, 2], [3, 4]]) for M in all_matrices]
    t = ()

    for mixin in all_mixins:
        for M in Ms:
            with warns_deprecated_sympy():
                assert isinstance(M, mixin) is True
        with warns_deprecated_sympy():
            assert isinstance(t, mixin) is False

