
def extract_shape_from_varargs(
    shape: ShapeType | tuple[ShapeType],
    validate=True,
) -> tuple[int, ...]:
    """
    Returns a shape from varargs.

    In PyTorch, operations that accept shapes often accept them as varargs, like
    foo(*shape). However a user can pass the shape as a sequence of integers,
    like this:

      foo(1, 2, 3)

    or as a sequence of integers

      foo((1, 2, 3))

    In the first case shape will be a tuple of integers, and in the second case it's a tuple
    containing a tuple of integers. This validates those inputs and canonicalizes them
    to a tuple of integers.
    """

    # Handles tuple unwrapping
    if len(shape) == 1 and isinstance(shape[0], Sequence):
        # pyrefly: ignore [bad-assignment]
        shape = shape[0]

    if validate:
        validate_shape(shape)  # type: ignore[arg-type]
    return shape  # type: ignore[return-value]

