
def test_issue_15791():
    class CrashingCodePrinter(CodePrinter):
        def emptyPrinter(self, obj):
            raise NotImplementedError

    from sympy.matrices import (
        MutableSparseMatrix,
        ImmutableSparseMatrix,
    )

    c = CrashingCodePrinter()

    # these should not silently succeed
    with raises(PrintMethodNotImplementedError):
        c.doprint(ImmutableSparseMatrix(2, 2, {}))
    with raises(PrintMethodNotImplementedError):
        c.doprint(MutableSparseMatrix(2, 2, {}))

