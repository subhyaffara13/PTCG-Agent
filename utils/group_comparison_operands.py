
def group_comparison_operands(
    pairwise_comparisons: Iterable[tuple[str, Expression, Expression]],
    operand_to_literal_hash: Mapping[int, Key],
    operators_to_group: set[str],
) -> list[tuple[str, list[int]]]:
    """Group a series of comparison operands together chained by any operand
    in the 'operators_to_group' set. All other pairwise operands are kept in
    groups of size 2.

    For example, suppose we have the input comparison expression:

        x0 == x1 == x2 < x3 < x4 is x5 is x6 is not x7 is not x8

    If we get these expressions in a pairwise way (e.g. by calling ComparisonExpr's
    'pairwise()' method), we get the following as input:

        [('==', x0, x1), ('==', x1, x2), ('<', x2, x3), ('<', x3, x4),
         ('is', x4, x5), ('is', x5, x6), ('is not', x6, x7), ('is not', x7, x8)]

    If `operators_to_group` is the set {'==', 'is'}, this function will produce
    the following "simplified operator list":

       [("==", [0, 1, 2]), ("<", [2, 3]), ("<", [3, 4]),
        ("is", [4, 5, 6]), ("is not", [6, 7]), ("is not", [7, 8])]

    Note that (a) we yield *indices* to the operands rather then the operand
    expressions themselves and that (b) operands used in a consecutive chain
    of '==' or 'is' are grouped together.

    If two of these chains happen to contain operands with the same underlying
    literal hash (e.g. are assignable and correspond to the same expression),
    we combine those chains together. For example, if we had:

        same == x < y == same

    ...and if 'operand_to_literal_hash' contained the same values for the indices
    0 and 3, we'd produce the following output:

        [("==", [0, 1, 2, 3]), ("<", [1, 2])]

    But if the 'operand_to_literal_hash' did *not* contain an entry, we'd instead
    default to returning:

        [("==", [0, 1]), ("<", [1, 2]), ("==", [2, 3])]

    This function is currently only used to assist with type-narrowing refinements
    and is extracted out to a helper function so we can unit test it.
    """
    groups: dict[str, DisjointDict[Key, int]] = {op: DisjointDict() for op in operators_to_group}

    simplified_operator_list: list[tuple[str, list[int]]] = []
    last_operator: str | None = None
    current_indices: set[int] = set()
    current_hashes: set[Key] = set()
    for i, (operator, left_expr, right_expr) in enumerate(pairwise_comparisons):
        if last_operator is None:
            last_operator = operator

        if current_indices and (operator != last_operator or operator not in operators_to_group):
            # If some of the operands in the chain are assignable, defer adding it: we might
            # end up needing to merge it with other chains that appear later.
            if not current_hashes:
                simplified_operator_list.append((last_operator, sorted(current_indices)))
            else:
                groups[last_operator].add_mapping(current_hashes, current_indices)
            last_operator = operator
            current_indices = set()
            current_hashes = set()

        # Note: 'i' corresponds to the left operand index, so 'i + 1' is the
        # right operand.
        current_indices.add(i)
        current_indices.add(i + 1)

        # We only ever want to combine operands/combine chains for these operators
        if operator in operators_to_group:
            left_hash = operand_to_literal_hash.get(i)
            if left_hash is not None:
                current_hashes.add(left_hash)
            right_hash = operand_to_literal_hash.get(i + 1)
            if right_hash is not None:
                current_hashes.add(right_hash)

    if last_operator is not None:
        if not current_hashes:
            simplified_operator_list.append((last_operator, sorted(current_indices)))
        else:
            groups[last_operator].add_mapping(current_hashes, current_indices)

    # Now that we know which chains happen to contain the same underlying expressions
    # and can be merged together, add in this info back to the output.
    for operator, disjoint_dict in groups.items():
        for keys, indices in disjoint_dict.items():
            simplified_operator_list.append((operator, sorted(indices)))

    # For stability, reorder list by the first operand index to appear
    simplified_operator_list.sort(key=lambda item: item[1][0])
    return simplified_operator_list

