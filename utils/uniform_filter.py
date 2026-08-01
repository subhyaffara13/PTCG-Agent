
def uniform_filter(input, size=3, output=None, mode="reflect",
                   cval=0.0, origin=0, *, axes=None):
    """Multidimensional uniform filter.

    Parameters
    ----------
    %(input)s
    size : int or sequence of ints, optional
        The sizes of the uniform filter are given for each axis as a
        sequence, or as a single number, in which case the size is
        equal for all axes.
    %(output)s
    %(mode_multiple)s
    %(cval)s
    %(origin_multiple)s
    axes : tuple of int or None, optional
        If None, `input` is filtered along all axes. Otherwise,
        `input` is filtered along the specified axes. When `axes` is
        specified, any tuples used for `size`, `origin`, and/or `mode`
        must match the length of `axes`. The ith entry in any of these tuples
        corresponds to the ith entry in `axes`.

    Returns
    -------
    uniform_filter : ndarray
        Filtered array. Has the same shape as `input`.

    Notes
    -----
    The multidimensional filter is implemented as a sequence of
    1-D uniform filters. The intermediate arrays are stored
    in the same data type as the output. Therefore, for output types
    with a limited precision, the results may be imprecise because
    intermediate results may be stored with insufficient precision.

    %(nan)s

    Examples
    --------
    >>> from scipy import ndimage, datasets
    >>> import matplotlib.pyplot as plt
    >>> fig = plt.figure()
    >>> plt.gray()  # show the filtered result in grayscale
    >>> ax1 = fig.add_subplot(121)  # left side
    >>> ax2 = fig.add_subplot(122)  # right side
    >>> ascent = datasets.ascent()
    >>> result = ndimage.uniform_filter(ascent, size=20)
    >>> ax1.imshow(ascent)
    >>> ax2.imshow(result)
    >>> plt.show()
    """
    input = np.asarray(input)
    output = _ni_support._get_output(output, input,
                                     complex_output=input.dtype.kind == 'c')
    axes = _ni_support._check_axes(axes, input.ndim)
    num_axes = len(axes)
    sizes = _ni_support._normalize_sequence(size, num_axes)
    origins = _ni_support._normalize_sequence(origin, num_axes)
    modes = _ni_support._normalize_sequence(mode, num_axes)
    axes = [(axes[ii], sizes[ii], origins[ii], modes[ii])
            for ii in range(num_axes) if sizes[ii] > 1]
    if len(axes) > 0:
        for axis, size, origin, mode in axes:
            uniform_filter1d(input, int(size), axis, output, mode,
                             cval, origin)
            input = output
    else:
        output[...] = input[...]
    return output


def uniform_filter(player_policies, selection_probabilities, player,
                   effective_number_to_select, solver):
  """Returns 'effective_number_to_select' uniform-randomly selected policies.

  Args:
    player_policies: A list of policies for the current player.
    selection_probabilities: Selection probabilities for 'player_policies'.
    player: Player id.
    effective_number_to_select: Effective number of policies to select.
    solver: PSRO solver instance if kwargs needed.

  Returns:
    selected_policies : List of size 'effective_number_to_select'
      containing selected policies.
    selected_indexes: List of the same shape as selected_policies,
      containing the list indexes of selected policies.
  """
  del solver, selection_probabilities, player
  selected_indexes = list(
      np.random.choice(
          list(range(len(player_policies))),
          effective_number_to_select,
          replace=False,
          p=np.ones(len(player_policies)) / len(player_policies)))
  selected_policies = [player_policies[i] for i in selected_indexes]
  return selected_policies, selected_indexes

