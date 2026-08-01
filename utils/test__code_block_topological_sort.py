
def test_CodeBlock_topological_sort():
    assignments = [
        Assignment(x, y + z),
        Assignment(z, 1),
        Assignment(t, x),
        Assignment(y, 2),
        ]

    ordered_assignments = [
        # Note that the unrelated z=1 and y=2 are kept in that order
        Assignment(z, 1),
        Assignment(y, 2),
        Assignment(x, y + z),
        Assignment(t, x),
        ]
    c1 = CodeBlock.topological_sort(assignments)
    assert c1 == CodeBlock(*ordered_assignments)

    # Cycle
    invalid_assignments = [
        Assignment(x, y + z),
        Assignment(z, 1),
        Assignment(y, x),
        Assignment(y, 2),
        ]

    raises(ValueError, lambda: CodeBlock.topological_sort(invalid_assignments))

    # Free symbols
    free_assignments = [
        Assignment(x, y + z),
        Assignment(z, a * b),
        Assignment(t, x),
        Assignment(y, b + 3),
        ]

    free_assignments_ordered = [
        Assignment(z, a * b),
        Assignment(y, b + 3),
        Assignment(x, y + z),
        Assignment(t, x),
        ]

    c2 = CodeBlock.topological_sort(free_assignments)
    assert c2 == CodeBlock(*free_assignments_ordered)

