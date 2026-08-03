from typing import Any, Dict, Optional

def block(arrays):
    """
    Assemble an nd-array from nested lists of blocks.

    Blocks in the innermost lists are concatenated (see `concatenate`) along
    the last dimension (-1), then these are concatenated along the
    second-last dimension (-2), and so on until the outermost list is reached.

    Blocks can be of any dimension, but will not be broadcasted using
    the normal rules. Instead, leading axes of size 1 are inserted,
    to make ``block.ndim`` the same for all blocks. This is primarily useful
    for working with scalars, and means that code like ``np.block([v, 1])``
    is valid, where ``v.ndim == 1``.

    When the nested list is two levels deep, this allows block matrices to be
    constructed from their components.

    Parameters
    ----------
    arrays : nested list of array_like or scalars (but not tuples)
        If passed a single ndarray or scalar (a nested list of depth 0), this
        is returned unmodified (and not copied).

        Elements shapes must match along the appropriate axes (without
        broadcasting), but leading 1s will be prepended to the shape as
        necessary to make the dimensions match.

    Returns
    -------
    block_array : ndarray
        The array assembled from the given blocks.

        The dimensionality of the output is equal to the greatest of:

        * the dimensionality of all the inputs
        * the depth to which the input list is nested

    Raises
    ------
    ValueError
        * If list depths are mismatched - for instance, ``[[a, b], c]`` is
          illegal, and should be spelt ``[[a, b], [c]]``
        * If lists are empty - for instance, ``[[a, b], []]``

    See Also
    --------
    concatenate : Join a sequence of arrays along an existing axis.
    stack : Join a sequence of arrays along a new axis.
    vstack : Stack arrays in sequence vertically (row wise).
    hstack : Stack arrays in sequence horizontally (column wise).
    dstack : Stack arrays in sequence depth wise (along third axis).
    column_stack : Stack 1-D arrays as columns into a 2-D array.
    vsplit : Split an array into multiple sub-arrays vertically (row-wise).
    unstack : Split an array into a tuple of sub-arrays along an axis.

    Notes
    -----
    When called with only scalars, ``np.block`` is equivalent to an ndarray
    call. So ``np.block([[1, 2], [3, 4]])`` is equivalent to
    ``np.array([[1, 2], [3, 4]])``.

    This function does not enforce that the blocks lie on a fixed grid.
    ``np.block([[a, b], [c, d]])`` is not restricted to arrays of the form::

        AAAbb
        AAAbb
        cccDD

    But is also allowed to produce, for some ``a, b, c, d``::

        AAAbb
        AAAbb
        cDDDD

    Since concatenation happens along the last axis first, `block` is *not*
    capable of producing the following directly::

        AAAbb
        cccbb
        cccDD

    Matlab's "square bracket stacking", ``[A, B, ...; p, q, ...]``, is
    equivalent to ``np.block([[A, B, ...], [p, q, ...]])``.

    Examples
    --------
    The most common use of this function is to build a block matrix:

    >>> import numpy as np
    >>> A = np.eye(2) * 2
    >>> B = np.eye(3) * 3
    >>> np.block([
    ...     [A,               np.zeros((2, 3))],
    ...     [np.ones((3, 2)), B               ]
    ... ])
    array([[2., 0., 0., 0., 0.],
           [0., 2., 0., 0., 0.],
           [1., 1., 3., 0., 0.],
           [1., 1., 0., 3., 0.],
           [1., 1., 0., 0., 3.]])

    With a list of depth 1, `block` can be used as `hstack`:

    >>> np.block([1, 2, 3])              # hstack([1, 2, 3])
    array([1, 2, 3])

    >>> a = np.array([1, 2, 3])
    >>> b = np.array([4, 5, 6])
    >>> np.block([a, b, 10])             # hstack([a, b, 10])
    array([ 1,  2,  3,  4,  5,  6, 10])

    >>> A = np.ones((2, 2), int)
    >>> B = 2 * A
    >>> np.block([A, B])                 # hstack([A, B])
    array([[1, 1, 2, 2],
           [1, 1, 2, 2]])

    With a list of depth 2, `block` can be used in place of `vstack`:

    >>> a = np.array([1, 2, 3])
    >>> b = np.array([4, 5, 6])
    >>> np.block([[a], [b]])             # vstack([a, b])
    array([[1, 2, 3],
           [4, 5, 6]])

    >>> A = np.ones((2, 2), int)
    >>> B = 2 * A
    >>> np.block([[A], [B]])             # vstack([A, B])
    array([[1, 1],
           [1, 1],
           [2, 2],
           [2, 2]])

    It can also be used in place of `atleast_1d` and `atleast_2d`:

    >>> a = np.array(0)
    >>> b = np.array([1])
    >>> np.block([a])                    # atleast_1d(a)
    array([0])
    >>> np.block([b])                    # atleast_1d(b)
    array([1])

    >>> np.block([[a]])                  # atleast_2d(a)
    array([[0]])
    >>> np.block([[b]])                  # atleast_2d(b)
    array([[1]])


    """
    arrays, list_ndim, result_ndim, final_size = _block_setup(arrays)

    # It was found through benchmarking that making an array of final size
    # around 256x256 was faster by straight concatenation on a
    # i7-7700HQ processor and dual channel ram 2400MHz.
    # It didn't seem to matter heavily on the dtype used.
    #
    # A 2D array using repeated concatenation requires 2 copies of the array.
    #
    # The fastest algorithm will depend on the ratio of CPU power to memory
    # speed.
    # One can monitor the results of the benchmark
    # https://pv.github.io/numpy-bench/#bench_shape_base.Block2D.time_block2d
    # to tune this parameter until a C version of the `_block_info_recursion`
    # algorithm is implemented which would likely be faster than the python
    # version.
    if list_ndim * final_size > (2 * 512 * 512):
        return _block_slicing(arrays, list_ndim, result_ndim)
    else:
        return _block_concatenate(arrays, list_ndim, result_ndim)


def block(state: StateCore) -> None:
    if state.inlineMode:
        token = Token("inline", "", 0)
        token.content = state.src
        token.map = [0, 1]
        token.children = []
        state.tokens.append(token)
    else:
        state.md.block.parse(state.src, state.md, state.env, state.tokens)


def block(
    reason: str, detection_info: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Block the request/response with a reason.

    Args:
        reason: Human-readable reason for blocking
        detection_info: Optional additional detection metadata

    Returns:
        Dict indicating the request should be blocked
    """
    result: Dict[str, Any] = {"action": "block", "reason": reason}
    if detection_info:
        result["detection_info"] = detection_info
    return result


def block(arrays: ArrayLike | list[ArrayLike]) -> Array:
  """Create an array from a list of blocks.

  JAX implementation of :func:`numpy.block`.

  Args:
    arrays: an array, or nested list of arrays which will be concatenated
      together to form the final array.

  Returns:
    a single array constructed from the inputs.

  See also:
    - :func:`concatenate`, :func:`concat`: concatenate arrays along an existing axis.
    - :func:`stack`, :func:`vstack`, :func:`hstack`, :func:`dstack` concatenate
      arrays along a new axis.

  Examples:
    consider these blocks:

    >>> zeros = jnp.zeros((2, 2))
    >>> ones = jnp.ones((2, 2))
    >>> twos = jnp.full((2, 2), 2)
    >>> threes = jnp.full((2, 2), 3)

    Passing a single array to :func:`block` returns the array:

    >>> jnp.block(zeros)
    Array([[0., 0.],
           [0., 0.]], dtype=float32)

    Passing a simple list of arrays concatenates them along the last axis:

    >>> jnp.block([zeros, ones])
    Array([[0., 0., 1., 1.],
           [0., 0., 1., 1.]], dtype=float32)

    Passing a doubly-nested list of arrays concatenates the inner list along
    the last axis, and the outer list along the second-to-last axis:

    >>> jnp.block([[zeros, ones],
    ...            [twos, threes]])
    Array([[0., 0., 1., 1.],
           [0., 0., 1., 1.],
           [2., 2., 3., 3.],
           [2., 2., 3., 3.]], dtype=float32)

    Note that blocks need not align in all dimensions, though the size along the axis
    of concatenation must match. For example, this is valid because after the inner,
    horizontal concatenation, the resulting blocks have a valid shape for the outer,
    vertical concatenation.

    >>> a = jnp.zeros((2, 1))
    >>> b = jnp.ones((2, 3))
    >>> c = jnp.full((1, 2), 2)
    >>> d = jnp.full((1, 2), 3)
    >>> jnp.block([[a, b], [c, d]])
    Array([[0., 1., 1., 1.],
           [0., 1., 1., 1.],
           [2., 2., 3., 3.]], dtype=float32)

    Note also that this logic generalizes to blocks in 3 or more dimensions.
    Here's a 3-dimensional block-wise array:

    >>> x = jnp.arange(6).reshape((1, 2, 3))
    >>> blocks = [[[x for i in range(3)] for j in range(4)] for k in range(5)]
    >>> jnp.block(blocks).shape
    (5, 8, 9)
  """
  out, _ = _block(arrays)
  return out


def block(char):
    """Return the block property assigned to the Unicode character 'char'
    as a string.

    >>> block("a")
    'Basic Latin'
    >>> block(chr(0x060C))
    'Arabic'
    >>> block(chr(0xEFFFF))
    'No_Block'
    """
    code = byteord(char)
    i = bisect_right(Blocks.RANGES, code)
    return Blocks.VALUES[i - 1]

