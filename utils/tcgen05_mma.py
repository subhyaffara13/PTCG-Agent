
def tcgen05_mma(accumulator: _ods_ir.Value[_ods_ir.MemRefType], a: _ods_ir.Value[_ods_ir.MemRefType], b: _ods_ir.Value[_ods_ir.MemRefType], accumulate: _ods_ir.Value[_ods_ir.IntegerType], *, a_scale: _Optional[_ods_ir.Value[_ods_ir.MemRefType]] = None, b_scale: _Optional[_ods_ir.Value[_ods_ir.MemRefType]] = None, a_sparse_metadata: _Optional[_ods_ir.Value[_ods_ir.MemRefType]] = None, collective: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> TcGen05MMAOp:
  return TcGen05MMAOp(accumulator=accumulator, a=a, b=b, accumulate=accumulate, a_scale=a_scale, b_scale=b_scale, a_sparse_metadata=a_sparse_metadata, collective=collective, loc=loc, ip=ip)


def tcgen05_mma(kind: _Union[_Any, _ods_ir.Attribute], cta_group: _Union[_Any, _ods_ir.Attribute], matrix_d: _ods_ir.Value, matrix_a: _ods_ir.Value, matrix_b: _ods_ir.Value[_ods_ir.IntegerType], idesc: _ods_ir.Value[_ods_ir.IntegerType], enable_input_d: _ods_ir.Value[_ods_ir.IntegerType], *, collector_op: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, a_shift: _Optional[bool] = None, scale_input_d: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, disable_output_lane: _Optional[_ods_ir.Value[_ods_ir.VectorType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> Tcgen05MMAOp:
  return Tcgen05MMAOp(kind=kind, ctaGroup=cta_group, matrixD=matrix_d, matrixA=matrix_a, matrixB=matrix_b, idesc=idesc, enableInputD=enable_input_d, collectorOp=collector_op, aShift=a_shift, scaleInputD=scale_input_d, disableOutputLane=disable_output_lane, loc=loc, ip=ip)


def tcgen05_mma(acc: _Ref,
                a: _Ref,
                b: _Ref,
                barrier: _Ref | None = None,
                *,
                a_scale: _Ref | None = None,
                b_scale: _Ref | None = None,
                a_sparse_metadata: _Ref | None = None,
                accumulate: bool | jax.Array = True,
                collective_axis: str | None = None):
  """Asynchronous matrix-multiply accumulate for TensorCore gen 5 (Blackwell).

  If run in collective mode, ``acc``, ``a`` (LHS), and ``b`` (RHS) should
  correspond to half of the total inputs to the MMA, where ``acc`` and ``a``
  (LHS) are split in half along the rows and ``b`` (RHS) is split along the
  columns like so::

    -----------    -----------   -----------
    |  ACC1   |    |  LHS1   |   |    |    |
    ----------- += ----------- @ |RHS1|RHS2|
    |  ACC2   |    |  LHS2   |   |    |    |
    -----------    -----------   -----------

  To use the block-scaled matrix-multiply, provide ``a_scale`` and ``b_scale``
  operands (they must be both present or both unspecified).

  Args:
    acc: The accumulator. Must be a TMEM Ref.
    a: The left-hand side. Must be a TMEM/SMEM Ref.
    b: The right-hand side. Must be an SMEM Ref.
    barrier: Optional barrier Ref for synchronizing with the tensor core.
      Must have orders_tensor_core set to True. If not specified, the MMA
      completion should be explicitly observed by calling
      :func:`jax.experimental.pallas.mosaic_gpu.tcgen05_commit_arrive`
    a_scale: An optional scale for the ``a`` operand. Must be a TMEM Ref if present.
    b_scale: An optional scale for the ``b`` operand. Must be a TMEM Ref if present.
    a_sparse_metadata: An optional sparse metadata for the ``a`` operand.
      Must be a TMEM Ref if present.
    accumulate: Whether to accumulate into acc or overwrite it.
    collective_axis: The name of the cluster axis along which to perform
      a collective MMA. The cluster axis should have a size of exactly 2,
      and must be on the minormost cluster axis.
  """
  acc_m, acc_n = acc.shape
  lhs_m, lhs_k = a.shape
  rhs_k, rhs_n = b.shape
  is_sparse = a_sparse_metadata is not None

  if acc_m != lhs_m:
    raise ValueError(
        "Accumulator and LHS have incompatible shapes. Expected LHS to have"
        " shape (m, k) and accumulator to have shape (m, n). Accumulator:"
        f" {acc.shape}. LHS: {a.shape}."
    )

  if collective_axis is not None:
    if acc_n != rhs_n * 2:
      raise ValueError(
          "Accumulator and RHS have incompatible shapes. Expected RHS to have "
          "shape (k, n) and accumulator to have shape (m, n * 2) in "
          f"collective mode. Accumulator: {acc.shape}. RHS: {b.shape}."
      )
  elif acc_n != rhs_n:
    raise ValueError(
        "Accumulator and RHS have incompatible shapes. Expected RHS to have"
        " shape (k, n) and accumulator to have shape (m, n). Accumulator:"
        f" {acc.shape}. RHS: {b.shape}."
    )

  if (lhs_k * (1 + is_sparse)) != rhs_k:
    raise ValueError(
        f"LHS and RHS have incompatible shapes. LHS: {a.shape}. RHS: {b.shape}.")

  if isinstance(acc, pallas_core.TransformedRef):
    acc_transforms_leaves, acc_transforms_tree = jax.tree.flatten(
        acc.transforms)
    acc = acc.ref
  else:
    acc_transforms_leaves, acc_transforms_tree = [], None

  if isinstance(a, pallas_core.TransformedRef):
    a_transforms_leaves, a_transforms_tree = jax.tree.flatten(a.transforms)
    a = a.ref
  else:
    a_transforms_leaves, a_transforms_tree = [], None

  if isinstance(b, pallas_core.TransformedRef):
    b_transforms_leaves, b_transforms_tree = jax.tree.flatten(b.transforms)
    b = b.ref
  else:
    b_transforms_leaves, b_transforms_tree = [], None

  if (is_scaled := a_scale is not None) != (b_scale is not None):
    raise ValueError("a_scale and b_scale must both be present or absent.")
  scales = []
  if isinstance(a_scale, pallas_core.TransformedRef):
    a_scale_transforms_leaves, a_scale_transforms_tree = jax.tree.flatten(
        a_scale.transforms
    )
    scales.append(a_scale.ref)
  else:
    a_scale_transforms_leaves, a_scale_transforms_tree = [], None
    scales.append(a_scale)
  if isinstance(b_scale, pallas_core.TransformedRef):
    b_scale_transforms_leaves, b_scale_transforms_tree = jax.tree.flatten(
        b_scale.transforms
    )
    scales.append(b_scale.ref)
  else:
    b_scale_transforms_leaves, b_scale_transforms_tree = [], None
    scales.append(b_scale)
  if not is_scaled:
    scales = []

  if isinstance(a_sparse_metadata, pallas_core.TransformedRef):
    a_sparse_metadata_transforms_leaves, a_sparse_metadata_transforms_tree = jax.tree.flatten(
        a_sparse_metadata.transforms
    )
    sparse_metadata = [a_sparse_metadata.ref]
  else:
    a_sparse_metadata_transforms_leaves, a_sparse_metadata_transforms_tree = [], None
    sparse_metadata = [a_sparse_metadata] if is_sparse else []

  if isinstance(barrier, pallas_core.TransformedRef):
    barrier_transforms_leaves, barrier_transforms_tree = jax.tree.flatten(
        barrier.transforms
    )
    barrier = barrier.ref
  else:
    barrier_transforms_leaves, barrier_transforms_tree = [], None

  if barrier is not None:
    barrier_ref = [barrier]
    arrive = True
  else:
    barrier_ref = []
    arrive = False

  tcgen05_mma_p.bind(acc, a, b, accumulate, *barrier_ref, *scales, *sparse_metadata,
                     *acc_transforms_leaves, *a_transforms_leaves,
                     *b_transforms_leaves,
                     *barrier_transforms_leaves,
                     *a_scale_transforms_leaves, *b_scale_transforms_leaves,
                     *a_sparse_metadata_transforms_leaves,
                     acc_transforms_tree=acc_transforms_tree,
                     a_transforms_tree=a_transforms_tree,
                     b_transforms_tree=b_transforms_tree,
                     barrier_transforms_tree=barrier_transforms_tree,
                     a_scale_transforms_tree=a_scale_transforms_tree,
                     b_scale_transforms_tree=b_scale_transforms_tree,
                     a_sparse_metadata_transforms_tree=a_sparse_metadata_transforms_tree,
                     collective_axis=collective_axis,
                     arrive=arrive,
                     scaled=bool(scales),
                     sparse=is_sparse)

