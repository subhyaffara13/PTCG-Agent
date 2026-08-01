
def _dot_general_shape_rule(lhs, rhs, *, dimension_numbers, precision,
                            preferred_element_type: DTypeLike | None,
                            out_sharding):
  if out_sharding is not None and not isinstance(out_sharding, NamedSharding):
    raise NotImplementedError
  (lhs_contracting, rhs_contracting), (lhs_batch, rhs_batch) = _from_maybe_ragged(dimension_numbers)
  if not all(np.all(np.greater_equal(d, 0)) and np.all(np.less(d, lhs.ndim))
             for d in (lhs_contracting, lhs_batch)):
    msg = ("dot_general requires lhs dimension numbers to be nonnegative and "
           "less than the number of axes of the lhs value, got "
           f"lhs_batch of {lhs_batch} and lhs_contracting of {lhs_contracting} "
           f"for lhs of rank {lhs.ndim}")
    raise TypeError(msg)
  if not all(np.all(np.greater_equal(d, 0)) and np.all(np.less(d, rhs.ndim))
             for d in (rhs_contracting, rhs_batch)):
    msg = ("dot_general requires rhs dimension numbers to be nonnegative and "
           "less than the number of axes of the rhs value, got "
           f"rhs_batch of {rhs_batch} and rhs_contracting of {rhs_contracting} "
           f"for rhs of rank {rhs.ndim}")
    raise TypeError(msg)
  if len(lhs_batch) != len(rhs_batch):
    msg = ("dot_general requires equal numbers of lhs_batch and rhs_batch "
           "dimensions, got lhs_batch {} and rhs_batch {}.")
    raise TypeError(msg.format(lhs_batch, rhs_batch))
  lhs_contracting_set, lhs_batch_set = set(lhs_contracting), set(lhs_batch)
  rhs_contracting_set, rhs_batch_set = set(rhs_contracting), set(rhs_batch)
  if len(lhs_batch_set) != len(lhs_batch):
    msg = ("dot_general requires lhs batch dimensions to be distinct, got "
           f"lhs_batch {lhs_batch}.")
    raise TypeError(msg)
  if len(rhs_batch_set) != len(rhs_batch):
    msg = ("dot_general requires rhs batch dimensions to be distinct, got "
           f"rhs_batch {rhs_batch}.")
    raise TypeError(msg)
  if len(lhs_contracting_set) != len(lhs_contracting):
    msg = ("dot_general requires lhs contracting dimensions to be distinct, "
           f"got lhs_contracting {lhs_contracting}.")
    raise TypeError(msg)
  if len(rhs_contracting_set) != len(rhs_contracting):
    msg = ("dot_general requires rhs contracting dimensions to be distinct, "
           f"got rhs_contracting {rhs_contracting}.")
    raise TypeError(msg)
  if lhs_contracting_set & lhs_batch_set:
    msg = ("dot_general requires lhs batch dimensions to be disjoint from "
           "contracting dimensions, got lhs_batch {} and lhs_contracting {}.")
    raise TypeError(msg.format(lhs_batch, lhs_contracting))
  if rhs_contracting_set & rhs_batch_set:
    msg = ("dot_general requires rhs batch dimensions to be disjoint from "
           "contracting dimensions, got rhs_batch {} and rhs_contracting {}.")
    raise TypeError(msg.format(rhs_batch, rhs_contracting))
  lhs_batch_shape = tuple(lhs.shape[i] for i in lhs_batch)
  rhs_batch_shape = tuple(rhs.shape[i] for i in rhs_batch)
  if not core.definitely_equal_shape(lhs_batch_shape, rhs_batch_shape):
    msg = ("dot_general requires lhs batch dimensions and rhs batch dimensions "
           "to have the same shape, got {} and {}.")
    raise TypeError(msg.format(lhs_batch_shape, rhs_batch_shape))
  lhs_contracting_shape = tuple(lhs.shape[i] for i in lhs_contracting)
  rhs_contracting_shape = tuple(rhs.shape[i] for i in rhs_contracting)
  if not core.definitely_equal_shape(lhs_contracting_shape, rhs_contracting_shape):
    msg = ("dot_general requires contracting dimensions to have the same "
           "shape, got {} and {}.")
    raise TypeError(msg.format(lhs_contracting_shape, rhs_contracting_shape))

  return _dot_general_shape_computation(lhs.shape, rhs.shape, dimension_numbers)

