
def equally_sized_accessor(
    elements, n_simple, n_variadic, n_preceding_simple, n_preceding_variadic
):
    """
    Returns a starting position and a number of elements per variadic group
    assuming equally-sized groups and the given numbers of preceding groups.

      elements: a sequential container.
      n_simple: the number of non-variadic groups in the container.
      n_variadic: the number of variadic groups in the container.
      n_preceding_simple: the number of non-variadic groups preceding the current
          group.
      n_preceding_variadic: the number of variadic groups preceding the current
          group.
    """

    total_variadic_length = len(elements) - n_simple
    # This should be enforced by the C++-side trait verifier.
    assert total_variadic_length % n_variadic == 0

    elements_per_group = total_variadic_length // n_variadic
    start = n_preceding_simple + n_preceding_variadic * elements_per_group
    return start, elements_per_group

