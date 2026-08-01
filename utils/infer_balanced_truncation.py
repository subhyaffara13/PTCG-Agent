
def infer_balanced_truncation(
    shape: Sequence[int],
    maximum_size: int,
    cutoff_size_per_axis: int,
    minimum_edge_items: int,
    doubling_bonus: float = 10.0,
) -> tuple[int | None, ...]:
  """Infers a balanced truncation from a shape.

  This function computes a set of truncation sizes for each axis of the array
  such that it obeys the constraints about array and axis sizes, while also
  keeping the relative proportions of the array consistent (e.g. we keep more
  elements along axes that were originally longer). This means that the aspect
  ratio of the truncated array will still resemble the aspect ratio of the
  original array.

  To avoid very-unbalanced renderings and truncate longer axes more than short
  ones, this function truncates based on the square-root of the axis size by
  default.

  Args:
    shape: The shape of the array we are truncating.
    maximum_size: Maximum number of elements of an array to show. Arrays larger
      than this will be truncated along one or more axes.
    cutoff_size_per_axis: Maximum number of elements of each individual axis to
      show without truncation. Any axis longer than this will be truncated, with
      their visual size increasing logarithmically with the true axis size
      beyond this point.
    minimum_edge_items: How many values to keep along each axis for truncated
      arrays. We may keep more than this up to the budget of maximum_size.
    doubling_bonus: Number of elements to add to each axis each time it doubles
      beyond `cutoff_size_per_axis`. Used to make longer axes appear visually
      longer while still keeping them a reasonable size.

  Returns:
    A tuple of edge sizes. Each element corresponds to an axis in `shape`,
    and is either `None` (for no truncation) or an integer (corresponding to
    the number of elements to keep at the beginning and at the end).
  """
  shape_arr = np.array(list(shape))
  remaining_elements_to_divide = maximum_size
  edge_items_per_axis = {}
  # Order our shape from smallest to largest, since the smallest axes will
  # require the least amount of truncation and will have the most stringent
  # constraints.
  sorted_axes = np.argsort(shape_arr)
  sorted_shape = shape_arr[sorted_axes]

  # Figure out maximum sizes based on the cutoff
  cutoff_adjusted_maximum_sizes = np.where(
      sorted_shape <= cutoff_size_per_axis,
      sorted_shape,
      cutoff_size_per_axis
      + doubling_bonus * np.log2(sorted_shape / cutoff_size_per_axis),
  )

  # Suppose we want to make a scaled version of the array with relative
  # axis sizes
  #   s0, s1, s2, ...
  # The total size is then
  #   size = (c * s0) * (c * s1) * (c * s2) * ...
  #   log(size) = ndim * log(c) + [ log s0 + log s1 + log s2 + ... ]
  # If we have a known final size we want to reach, we can solve for c as
  #   c = exp( (log size - [ log s0 + log s1 + log s2 + ... ]) / ndim )
  axis_proportions = np.sqrt(sorted_shape)
  log_axis_proportions = np.log(axis_proportions)
  for i in range(len(sorted_axes)):
    original_axis = sorted_axes[i]
    size = shape_arr[original_axis]
    # If we truncated this axis and every axis after it proportional to
    # their weights, how small of an axis size would we need for this
    # axis?
    log_c = (
        np.log(remaining_elements_to_divide) - np.sum(log_axis_proportions[i:])
    ) / (len(shape) - i)
    soft_limit_for_this_axis = np.exp(log_c + log_axis_proportions[i])
    cutoff_limit_for_this_axis = np.floor(
        np.minimum(
            soft_limit_for_this_axis,
            cutoff_adjusted_maximum_sizes[i],
        )
    )
    if size <= 2 * minimum_edge_items + 1 or size <= cutoff_limit_for_this_axis:
      # If this axis is already smaller than the minimum size it would have
      # after truncation, there's no reason to truncate it.
      # But pretend we did, so that other axes still grow monotonically if
      # their axis sizes increase.
      remaining_elements_to_divide = (
          remaining_elements_to_divide / soft_limit_for_this_axis
      )
      edge_items_per_axis[original_axis] = None
    elif cutoff_limit_for_this_axis < 2 * minimum_edge_items + 1:
      # If this axis is big enough to truncate, but our naive target size is
      # smaller than the minimum allowed truncation, we should truncate it
      # to the minimum size allowed instead.
      edge_items_per_axis[original_axis] = minimum_edge_items
      remaining_elements_to_divide = remaining_elements_to_divide / (
          2 * minimum_edge_items + 1
      )
    else:
      # Otherwise, truncate it and all remaining axes based on our target
      # truncations.
      for j in range(i, len(sorted_axes)):
        visual_size = np.floor(
            np.minimum(
                np.exp(log_c + log_axis_proportions[j]),
                cutoff_adjusted_maximum_sizes[j],
            )
        )
        edge_items_per_axis[sorted_axes[j]] = int(visual_size // 2)
      break

  return tuple(
      edge_items_per_axis[orig_axis] for orig_axis in range(len(shape))
  )

