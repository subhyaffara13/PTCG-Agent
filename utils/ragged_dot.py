
def ragged_dot(result: _ods_ir.Type, lhs: _ods_ir.Value, rhs: _ods_ir.Value, group_sizes: _ods_ir.Value[_ods_ir.RankedTensorType], ragged_dot_dimension_numbers: _Union[_Any, _ods_ir.Attribute], *, precision_config: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return RaggedDotOp(result=result, lhs=lhs, rhs=rhs, group_sizes=group_sizes, ragged_dot_dimension_numbers=ragged_dot_dimension_numbers, precision_config=precision_config, loc=loc, ip=ip).result


def ragged_dot(result: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.RankedTensorType], rhs: _ods_ir.Value[_ods_ir.RankedTensorType], group_sizes: _ods_ir.Value[_ods_ir.RankedTensorType], ragged_dot_dimension_numbers: _Union[_Any, _ods_ir.Attribute], *, precision_config: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.RankedTensorType]:
  return RaggedDotOp(result=result, lhs=lhs, rhs=rhs, group_sizes=group_sizes, ragged_dot_dimension_numbers=ragged_dot_dimension_numbers, precision_config=precision_config, loc=loc, ip=ip).result


def ragged_dot(
    lhs,
    rhs,
    group_sizes,
):
  """Reference ragged dot implementation."""
  m, lk = lhs.shape
  group_count, rk, n = rhs.shape
  assert lk == rk
  assert group_count == group_sizes.shape[0]
  assert lhs.dtype == rhs.dtype

  out = np.zeros((m, n), dtype=lhs.dtype)
  result_iota = np.expand_dims(np.arange(out.shape[0]), list(range(1, out.ndim)))
  result_iota = result_iota.astype(group_sizes.dtype)
  start = np.asarray(0, dtype=group_sizes.dtype)
  for i, size in enumerate(group_sizes):
    out += np.where(
        np.logical_and(start <= result_iota, result_iota < (start + size)),
        np.einsum(
          "nk,km->nm",
          lhs,
          rhs[i, :, :],
          dtype=np.float32 if lhs.dtype == dtypes.bfloat16 else None,
        ),
        np.zeros(out.shape, dtype=out.dtype),
    )
    start += size
  return out.astype(dtypes.bfloat16) if lhs.dtype == dtypes.bfloat16 else out


def ragged_dot(
    lhs: Array,
    rhs: Array,
    group_sizes: Array,
    precision: PrecisionLike = None,
    preferred_element_type: DTypeLike | None = None,
    group_offset: Array | None = None,
    out_sharding: NamedSharding | P | None = None,
    ) -> Array:
  """Ragged matrix multiplication.

  Args:
    lhs: (m, k) shaped array.
    rhs: (g, k, n) shaped array.
    group_sizes: (g,) shaped array with integer element type, where g denotes   number of groups. The ith element indicates the size of ith group.
    precision: Optional. Consistent with precision argument for :func:`jax.lax.dot`.
    preferred_element_type: Optional. Consistent with precision argument for :func:`jax.lax.dot`.
    group_offset: Optional. (1,) shaped array that indicates the group in group_sizes to start computing from. If not specified, defaults to [0].

  Results:
    (m, n) shaped array with preferred_element_type element type.
  """
  return ragged_dot_general(
      lhs,
      rhs,
      group_sizes,
      ragged_dot_dimension_numbers=_BASIC_RAGGED_DOT_DIMENSION_NUMBERS,
      precision=canonicalize_precision(precision),
      preferred_element_type=preferred_element_type,
      group_offset=group_offset,
      out_sharding=out_sharding,
  )


def ragged_dot(
    lhs,  # (M, K)
    rhs,  # (G, K, N)
    *,
    group_sizes,  # (G,)
    block_m: int,
    block_n: int,
    block_k: int,
    max_concurrent_steps: int,
    grid_block_n: int,
    transpose_rhs: bool = False,
    load_group_sizes_to_register: bool = True,
) -> jax.Array:
  if lhs.dtype != rhs.dtype:
    raise NotImplementedError(
        f"lhs and rhs must have the same dtype, got {lhs.dtype} and {rhs.dtype}"
    )
  m, k = lhs.shape
  g, k2, n = rhs.shape

  if transpose_rhs:
    k2, n = n, k2

  if group_sizes.shape[0] != g:
    raise ValueError(
        f"Expected group_sizes to have shape {g} but got {group_sizes.shape}"
    )

  if k != k2:
    raise ValueError(f"lhs.shape={k} must match rhs.shape={k2}")

  if k % block_k != 0:
    raise ValueError(f"k={k} must be a multiple of block_k={block_k}")

  def body(rows_per_expert_gmem, lhs_gmem, rhs_gmem, o_gmem):
    grid_m = pl.cdiv(m, block_m) + g - 1
    grid_n = pl.cdiv(n, block_n)
    grid = (grid_m * grid_n,)

    @plgpu.nd_loop(grid, collective_axes="sm")
    def mn_loop(loop_info: plgpu.NDLoopInfo):
      mi, ni = plgpu.planar_snake(
          loop_info.index[0],
          (grid_m, grid_n),
          1,
          grid_block_n,
      )
      group_info = GroupInfo.create(rows_per_expert_gmem, block_m, mi)

      def acc_scope(acc_ref):
        plgpu.emit_pipeline(
            lambda _, lhs_smem, rhs_smem: plgpu.wgmma(
                acc_ref,
                lhs_smem,
                plgpu.transpose_ref(rhs_smem, (1, 0)) if transpose_rhs else rhs_smem,
            ),
            grid=(k // block_k,),
            in_specs=[
                plgpu.BlockSpec(
                    (block_m, block_k),
                    lambda k: (group_info.block, k),
                    delay_release=1,
                ),
                plgpu.BlockSpec(
                    (block_n, block_k) if transpose_rhs else (block_k, block_n),
                    lambda k: (ni, k) if transpose_rhs else (k, ni),
                    delay_release=1,
                ),
            ],
            max_concurrent_steps=max_concurrent_steps,
        )(lhs_gmem, rhs_gmem.at[group_info.group_id])
        return acc_ref[...]

      acc = pl.run_scoped(acc_scope, plgpu.ACC((block_m, block_n)))

      @functools.partial(
          pl.run_scoped,
          o_smem=plgpu.SMEM((block_m, block_n), dtype=o_gmem.dtype)
      )
      def store_scope(o_smem):
        o_smem[...] = acc.astype(o_smem.dtype)
        plgpu.commit_smem()

        smem_start = group_info.start_within_block
        remaining_rows = min(block_m, m)
        # TMA descriptors need to be generated with static tile sizes along each
        # axis, but we do not know at compile time how many rows we will need to
        # store. We only know that the number of rows to store is bounded by
        # min(block_m, m).
        #
        # In order to work around that, we construct a logarithmic ladder of
        # TMA descriptors, where each descriptor can store 2**i rows for some
        # i between 0 and log2(min(block_m, m)). This allows storing any
        # number of rows we will need to store, so long as this number of rows
        # is between `1` and `min(block_m, m)`.
        #
        # E.g., imagine we have block_m = 8, m = 16. The loop below will be
        # unrolled into 4 iterations, where the first one will generate a TMA
        # descriptor that can store 8 rows, the second one will generate a TMA
        # descriptor that can store 4 rows, etc. all the way to 1 row.
        #
        # At run time, we finally know the actual number of rows we need to
        # store as we go through the unrolled loop iterations. Let's imagine
        # that we need to store 5 rows.
        #
        # The first unrolled iteration will check whether we can store 8 rows.
        # Since we only need to store 5 rows, we won't store anything then.
        #
        # The second unrolled iteration will check whether we can store 4 rows.
        # We're able to store 4 rows, and are left with a single remaining row.
        #
        # The fourth unrolled iteration will store the single remaining row, and
        # we end up with a storing scheme as follows for our 5 rows:
        #
        #     -----------------------------------------------------------
        #  0  |                                                         |
        #  1  |                                                         |
        #  2  |                       Store 4 rows                      |
        #  3  |                                                         |
        #     -----------------------------------------------------------
        #  4  |                       Store 1 row                       |
        #     -----------------------------------------------------------
        while remaining_rows > 0:
          const_rows_len = 1 << int(math.log2(remaining_rows))
          remaining_rows //= 2

          @pl.when(group_info.actual_size & const_rows_len != 0)
          def _():
            o_smem_slice = o_smem.at[pl.ds(smem_start, const_rows_len)]
            o_gref_slice = o_gmem.at[
                pl.ds(group_info.block_start + smem_start, const_rows_len),
                pl.ds(ni * block_n, block_n),
            ]
            plgpu.copy_smem_to_gmem(o_smem_slice, o_gref_slice)

          smem_start += group_info.actual_size & const_rows_len
        plgpu.wait_smem_to_gmem(0, wait_read_only=True)

  # There are 132 SMs on a H100 SXM GPU.
  num_sms = 132
  kernel = plgpu.kernel(
      body,
      out_type=jax.ShapeDtypeStruct((m, n), lhs.dtype),
      grid=(num_sms,),
      grid_names=("sm",),
      compiler_params=plgpu.CompilerParams(
          lowering_semantics=plgpu.LoweringSemantics.Warpgroup,
      ),
  )
  return kernel(group_sizes, lhs, rhs)

