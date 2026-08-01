
def test_Assignment_printing():
    assignment_classes = [
        Assignment,
        AddAugmentedAssignment,
        SubAugmentedAssignment,
        MulAugmentedAssignment,
        DivAugmentedAssignment,
        ModAugmentedAssignment,
    ]
    pairs = [
        (x, 2 * y + 2),
        (B[i], x),
        (A22, B22),
        (A[0, 0], x),
    ]

    for cls in assignment_classes:
        for lhs, rhs in pairs:
            a = cls(lhs, rhs)
            assert repr(a) == '%s(%s, %s)' % (cls.__name__, repr(lhs), repr(rhs))

