
def between_ops() -> list[AHOperation]:
    dims = ["m", "k", "n"]
    limits = [(1, 16), (17, 32), (33, 64), (65, 128), (129, 256)]
    ah_operations = []
    for dim in dims:
        for lower, upper in limits:
            between_op_fn = functools.partial(
                between_op, dim=dim, lower=lower, upper=upper
            )
            # using 'LEQ' instead of '<=' because '<=' cannot be exported to dot
            between_op_name = f"{lower}LEQ{dim}LEQ{upper}"
            ah_operations.append(
                AHOperation(between_op_name, between_op_fn, is_categorical=True)
            )
    return ah_operations

