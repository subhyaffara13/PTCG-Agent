from typing import Any, Union

def contract_expression(
    subscripts: str,
    *operands: Union[ArrayType, TensorShapeType],
    constants: Union[Collection[int], None] = ...,
    use_blas: bool = ...,
    optimize: OptimizeKind = ...,
    memory_limit: _MemoryLimit = ...,
    **kwargs: Any,
) -> ContractExpression: ...


def contract_expression(
    subscripts: Union[ArrayType, TensorShapeType],
    *operands: Union[ArrayType, TensorShapeType, Collection[int]],
    constants: Union[Collection[int], None] = ...,
    use_blas: bool = ...,
    optimize: OptimizeKind = ...,
    memory_limit: _MemoryLimit = ...,
    **kwargs: Any,
) -> ContractExpression: ...


def contract_expression(
    subscripts: Union[str, ArrayType, TensorShapeType],
    *shapes: Union[ArrayType, TensorShapeType, Collection[int]],
    constants: Union[Collection[int], None] = None,
    use_blas: bool = True,
    optimize: OptimizeKind = True,
    memory_limit: _MemoryLimit = None,
    **kwargs: Any,
) -> ContractExpression:
    """Generate a reusable expression for a given contraction with
    specific shapes, which can, for example, be cached.

    Parameters:

        subscripts: Specifies the subscripts for summation.
        shapes: Shapes of the arrays to optimize the contraction for.
        constants: The indices of any constant arguments in `shapes`, in which case the
            actual array should be supplied at that position rather than just a
            shape. If these are specified, then constant parts of the contraction
            between calls will be reused. Additionally, if a GPU-enabled backend is
            used for example, then the constant tensors will be kept on the GPU,
            minimizing transfers.
        kwargs: Passed on to `contract_path` or `einsum`. See `contract`.

    Returns:
        Callable with signature `expr(*arrays, out=None, backend='numpy')` where the array's shapes should match `shapes`.

    Notes:
        The `out` keyword argument should be supplied to the generated expression
        rather than this function.
        The `backend` keyword argument should also be supplied to the generated
        expression. If numpy arrays are supplied, if possible they will be
        converted to and back from the correct backend array type.
        The generated expression will work with any arrays which have
        the same rank (number of dimensions) as the original shapes, however, if
        the actual sizes are different, the expression may no longer be optimal.
        Constant operations will be computed upon the first call with a particular
        backend, then subsequently reused.

    Examples:
    Basic usage:

    ```python
    expr = contract_expression("ab,bc->ac", (3, 4), (4, 5))
    a, b = np.random.rand(3, 4), np.random.rand(4, 5)
    c = expr(a, b)
    np.allclose(c, a @ b)
    #> True
    ```

    Supply `a` as a constant:

    ```python
    expr = contract_expression("ab,bc->ac", a, (4, 5), constants=[0])
    expr
    #> <ContractExpression('[ab],bc->ac', constants=[0])>

    c = expr(b)
    np.allclose(c, a @ b)
    #> True
    ```

    """
    if not optimize:
        raise ValueError("Can only generate expressions for optimized contractions.")

    for arg in ("out", "backend"):
        if kwargs.get(arg, None) is not None:
            raise ValueError(
                f"'{arg}' should only be specified when calling a " "`ContractExpression`, not when building it."
            )

    if not isinstance(subscripts, str):
        subscripts, shapes = parser.convert_interleaved_input((subscripts,) + shapes)

    kwargs["_gen_expression"] = True

    # build dict of constant indices mapped to arrays
    constants = constants or ()
    constants_dict = {i: shapes[i] for i in constants}
    kwargs["_constants_dict"] = constants_dict

    # apart from constant arguments, make dummy arrays
    dummy_arrays = [s if i in constants else shape_only(s) for i, s in enumerate(shapes)]  # type: ignore

    return contract(
        subscripts, *dummy_arrays, use_blas=use_blas, optimize=optimize, memory_limit=memory_limit, **kwargs
    )

