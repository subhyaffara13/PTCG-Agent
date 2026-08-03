from typing import Any

def _einsum(*operands: Any, **kwargs: Any) -> ArrayType:
    """Base einsum, but with pre-parse for valid characters if a string is given."""
    fn = backends.get_func("einsum", kwargs.pop("backend", "numpy"))

    if not isinstance(operands[0], str):
        return fn(*operands, **kwargs)

    einsum_str, operands = operands[0], operands[1:]

    # Do we need to temporarily map indices into [a-z,A-Z] range?
    if not parser.has_valid_einsum_chars_only(einsum_str):
        # Explicitly find output str first so as to maintain order
        if "->" not in einsum_str:
            einsum_str += "->" + parser.find_output_str(einsum_str)

        einsum_str = parser.convert_to_valid_einsum_chars(einsum_str)

    kwargs = _filter_einsum_defaults(kwargs)  # type: ignore
    return fn(einsum_str, *operands, **kwargs)


def _einsum(
    operands: list[Array],
    contractions: Sequence[tuple[tuple[int, ...], frozenset[str], str]],
    precision,
    preferred_element_type,
    _dot_general=lax.dot_general,
    out_sharding=None,
):
  if preferred_element_type is None:
    preferred_element_type, output_weak_type = dtypes.result_type(
        *operands, return_weak_type_flag=True)
  else:
    preferred_element_type = dtypes.check_and_canonicalize_user_dtype(
        preferred_element_type, 'einsum'
    )
    output_weak_type = False

  def sum(x, axes, out_s):
    if dtypes.result_type(x, preferred_element_type) != x.dtype:
      x = x.astype(preferred_element_type)
    return lax.reduce(
        x, np.array(0, x.dtype), lax.add if x.dtype != bool else lax.bitwise_or,
        axes, out_s)

  def sum_uniques(operand, names, uniques, out_s=None):
    if uniques:
      axes = [names.index(name) for name in uniques]
      operand = sum(operand, axes, out_s)
      names = _removechars(names, uniques)
    return operand, names

  def sum_repeats(operand, names, counts, keep_names, out_s=None):
    for name, count in counts.items():
      if count > 1:
        axes = [i for i, n in enumerate(names) if n == name]
        eye = lax._delta(np.dtype('bool'), operand.shape, axes)
        operand = lax.select(eye, operand, lax.full_like(operand, 0))
        if name not in keep_names:
          operand = sum(operand, axes, out_s)
          names = names.replace(name, '')
        else:
          operand = sum(operand, axes[:-1], out_s)
          names = names.replace(name, '', count - 1)
    return operand, names

  def filter_singleton_dims(operand, names, other_shape, other_names):
    eq = core.definitely_equal
    keep = [not eq(operand.shape[i], 1) or j == -1 or eq(other_shape[j], 1)
            for i, j in enumerate(map(other_names.find, names))]
    sqez_axes, keep_axes = partition_list(keep, list(range(operand.ndim)))
    return lax.squeeze(operand, sqez_axes), "".join(names[i] for i in keep_axes)

  for operand_indices, contracted_names_set, einstr in contractions:
    contracted_names = sorted(contracted_names_set)
    input_str, result_names = einstr.split('->')
    input_names = input_str.split(',')

    # switch on the number of operands to be processed in this loop iteration.
    # every case here sets 'operand' and 'names'.
    if len(operand_indices) == 1:
      operand = operands.pop(operand_indices[0])
      names, = input_names
      counts = collections.Counter(names)
      # sum out unique contracted indices with a single reduce-sum
      uniques = [name for name in contracted_names if counts[name] == 1]
      operand, names = sum_uniques(operand, names, uniques, out_sharding)
      # for every repeated index, do a contraction against an identity matrix
      operand, names = sum_repeats(operand, names, counts, result_names,
                                   out_sharding)
    elif len(operand_indices) == 2:
      lhs, rhs = map(operands.pop, operand_indices)
      lhs_names, rhs_names = input_names

      # handle cases where one side of a contracting or batch dimension is 1
      # but its counterpart is not.
      lhs, lhs_names = filter_singleton_dims(lhs, lhs_names, np.shape(rhs),
                                             rhs_names)
      rhs, rhs_names = filter_singleton_dims(rhs, rhs_names, np.shape(lhs),
                                             lhs_names)

      lhs_counts = collections.Counter(lhs_names)
      rhs_counts = collections.Counter(rhs_names)

      # sum out unique contracted indices in lhs and rhs
      lhs_uniques = [name for name in contracted_names
                     if lhs_counts[name] == 1 and rhs_counts[name] == 0]
      lhs, lhs_names = sum_uniques(lhs, lhs_names, lhs_uniques)

      rhs_uniques = [name for name in contracted_names
                     if rhs_counts[name] == 1 and lhs_counts[name] == 0]
      rhs, rhs_names = sum_uniques(rhs, rhs_names, rhs_uniques)

      # for every repeated index, contract against an identity matrix
      lhs, lhs_names = sum_repeats(lhs, lhs_names, lhs_counts,
                                   result_names + rhs_names)
      rhs, rhs_names = sum_repeats(rhs, rhs_names, rhs_counts,
                                   result_names + lhs_names)

      lhs_or_rhs_names = set(lhs_names) | set(rhs_names)
      contracted_names = [x for x in contracted_names if x in lhs_or_rhs_names]
      lhs_and_rhs_names = set(lhs_names) & set(rhs_names)
      batch_names = [x for x in result_names if x in lhs_and_rhs_names]

      lhs_batch, rhs_batch = unzip2((lhs_names.find(n), rhs_names.find(n))
                                    for n in batch_names)

      # NOTE(mattjj): this can fail non-deterministically in python3, maybe
      # due to opt_einsum
      assert all(
        name in lhs_names and name in rhs_names and
        lhs.shape[lhs_names.index(name)] == rhs.shape[rhs_names.index(name)]
        for name in contracted_names), (
          "Incompatible reduction dimensions: "
          f"lhs.shape={lhs.shape} lhs_names={lhs_names} "
          f"rhs.shape={rhs.shape} rhs_names={rhs_names}")

      # contract using dot_general
      batch_names_str = ''.join(batch_names)
      lhs_cont, rhs_cont = unzip2((lhs_names.index(n), rhs_names.index(n))
                                  for n in contracted_names)
      deleted_names = batch_names_str + ''.join(contracted_names)
      remaining_lhs_names = _removechars(lhs_names, deleted_names)
      remaining_rhs_names = _removechars(rhs_names, deleted_names)
      # Try both orders of lhs and rhs, in the hope that one of them means we
      # don't need an explicit transpose. opt_einsum likes to contract from
      # right to left, so we expect (rhs,lhs) to have the best chance of not
      # needing a transpose.
      names = batch_names_str + remaining_rhs_names + remaining_lhs_names
      if names == result_names:
        dimension_numbers = ((rhs_cont, lhs_cont), (rhs_batch, lhs_batch))
        dot_out_sharding = ({} if out_sharding is None else
                            {'out_sharding': out_sharding})
        operand = _dot_general(rhs, lhs, dimension_numbers, precision,
                               preferred_element_type=preferred_element_type,
                               **dot_out_sharding)
      else:
        names = batch_names_str + remaining_lhs_names + remaining_rhs_names
        dimension_numbers = ((lhs_cont, rhs_cont), (lhs_batch, rhs_batch))
        out_sharding = (_get_inverse_sharding(out_sharding, names, result_names)
                        if out_sharding is not None and names != result_names
                        else out_sharding)
        dot_out_sharding = ({} if out_sharding is None else
                            {'out_sharding': out_sharding})
        operand = _dot_general(lhs, rhs, dimension_numbers, precision,
                                preferred_element_type=preferred_element_type,
                                **dot_out_sharding)
    else:
      raise NotImplementedError(
        "jax.numpy.einsum does not support simultaneous contraction of 3 or more"
        " operands. Typically this means you've passed an unsupported path to"
        " the einsum optimize parameter.")

    # the resulting 'operand' with axis labels 'names' should be a permutation
    # of the desired result
    assert len(names) == len(result_names) == len(set(names))
    assert set(names) == set(result_names)
    if names != result_names:
      perm = tuple(names.index(name) for name in result_names)
      operand = lax.transpose(operand, perm)
    operands.append(operand)  # used in next iteration
  return lax._convert_element_type(operands[0], preferred_element_type,
                                   output_weak_type)

