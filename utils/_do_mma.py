import functools
import itertools
from typing import Any

def _do_mma(
    d_addr: ir.Value,
    a_desc_or_addr: tuple[ir.Value, int] | ir.Value,  # TMEM address if a_k_stride is None
    b_desc: tuple[ir.Value, int],
    a_transpose: bool,
    b_transpose: bool,
    a_k_strides: tuple[tuple[int, ...], tuple[int, ...]] | None,
    b_k_strides: tuple[tuple[int, ...], tuple[int, ...]],
    a_scale_addr: ir.Value | None,
    b_scale_addr: ir.Value | None,
    b_scale_n_stride: int | None,
    a_scale_m_stride: int | None,
    a_sparse_addr: ir.Value | None,
    m: int,
    n: int,
    k: int,
    element_type: ir.Type,
    scale_element_type: ir.Type | None,
    d_type: ir.Type,
    accumulate: ir.Value,
    collective: bool,
) -> None:
  i1 = ir.IntegerType.get_signless(1)
  i32 = ir.IntegerType.get_signless(32)
  a_k_idx_tiling, a_k_strides = a_k_strides or (None, None)  # pyrefly: ignore[bad-assignment]
  b_k_idx_tiling, b_k_strides = b_k_strides  # pyrefly: ignore[bad-assignment]
  assert all(
      s % 16 == 0   # pyrefly: ignore[unsupported-operation]
      for s in itertools.chain(a_k_strides or (), b_k_strides)
  )
  assert (a_scale_addr is None) == (b_scale_addr is None)
  is_scaled = a_scale_addr is not None
  is_sparse = a_sparse_addr is not None
  elem_bitwidth = utils.bitwidth(element_type)
  instr_k = (1 + is_sparse) * 8 * 32 // elem_bitwidth
  packing = 8 * 4 // elem_bitwidth

  scale_steps = None
  kind = None
  if is_scaled:
    if isinstance(element_type, ir.Float8E5M2Type) or isinstance(
        element_type, ir.Float8E4M3FNType
    ):
      if scale_element_type != ir.Float8E8M0FNUType.get():
        raise ValueError(
            f"Scale element type mismatch: expected f8e8m0fnu, got {scale_element_type}"
        )
      kind = "mxf8f6f4.block_scale.scale_vec::1X"
      scale_steps = 4
      create_scaled_instr_descriptor = functools.partial(
          create_scaled_f8f6f4_instr_descriptor, scale_type=scale_element_type,
          sparse=is_sparse,
      )
    elif isinstance(element_type, ir.Float4E2M1FNType):
      assert not a_transpose and not b_transpose
      create_scaled_instr_descriptor = functools.partial(
          create_scaled_f4_instr_descriptor,
          scale_type=scale_element_type,
          sparse=is_sparse,
      )
      if scale_element_type == ir.Float8E8M0FNUType.get():
        kind = "mxf4.block_scale.scale_vec::2X"
        scale_steps = 2
      elif scale_element_type == ir.Float8E4M3FNType.get():
        kind = "mxf4nvf4.block_scale.scale_vec::4X"
        scale_steps = 1
    else:
      raise NotImplementedError(f"Unsupported element type for block scaling: {element_type}")
    extra_ptx = "[$5], [$6], "
    extra_constraints = ",r,r"
  else:
    if isinstance(element_type, ir.F16Type) or isinstance(
        element_type, ir.BF16Type
    ):
      kind = "f16"
    elif isinstance(element_type, ir.Float8E5M2Type):
      kind = "f8f6f4"
    elif isinstance(element_type, ir.Float8E4M3FNType):
      kind = "f8f6f4"
    elif (
        isinstance(element_type, ir.IntegerType)
        and element_type.width == 8
        and element_type.is_signless
    ):
      kind = "i8"
    else:
      raise NotImplementedError(
          f"Unsupported input element type: {element_type}"
      )
    extra_constraints = extra_ptx = ""

    def create_scaled_instr_descriptor(*args):
      raise NotImplementedError

  num_cta = 2 if collective else 1
  a_in_tmem = a_k_strides is None
  a_ptx = "[a_desc]" if a_in_tmem else "a_desc"
  sparse_mod = ".sp" if is_sparse else ""
  sparse_meta_ptx = ""
  if is_sparse:
    sparse_meta_idx = 5 + (2 if is_scaled else 0)
    sparse_meta_ptx = f"[${sparse_meta_idx}], "
    extra_constraints += ",r"
  sp_selector = None
  sparse_addr: tuple[Any, ...] = ()
  scales_addrs: tuple[Any, ...] = ()
  def _get_offset(idx: int, idx_tiling: tuple[int, ...], strides: tuple[int, ...]):
    assert len(idx_tiling) + 1 == len(strides)
    idxs = []
    for t in idx_tiling:
      idxs.append(idx // t)
      idx = idx % t
    idxs.append(idx)
    offset = sum(i * s for i, s in zip(idxs, strides, strict=True))
    return offset >> 4
  for k_step in range(k // instr_k):
    if is_sparse:
      assert a_sparse_addr is not None
      sparse_group_elems = 8 if elem_bitwidth == 4 else 4
      # Each sparse group has 2 entries, each TMEM column holds 16 i2 entries.
      meta_cols_per_instr = instr_k // sparse_group_elems * 2 // 16
      instrs_per_col_pair = 2 // meta_cols_per_instr
      sp_selector = k_step % instrs_per_col_pair
      sparse_addr = (
          arith.addi(
              a_sparse_addr, utils.c(k_step // instrs_per_col_pair * 2, i32)
          ),
      )
    if is_scaled:
      assert scale_steps is not None
      scale_vec_width = 4 // scale_steps
      scale_id = (k_step % scale_steps) * scale_vec_width
      assert sp_selector in {None, 0}  # Scaled instr descriptor has no selector
      i_desc = create_scaled_instr_descriptor(
          m * num_cta, n * num_cta, element_type, element_type,
          scale_id, scale_id, a_transpose, b_transpose
      )
      assert (m == 64 and collective) or m == 128
      assert (n * num_cta) % 32 == 0
      assert a_scale_addr is not None
      assert b_scale_addr is not None
      assert a_scale_m_stride is not None
      assert b_scale_n_stride is not None
      # A scales are sharded, B scales are replicated across CTAs.
      a_scale_addr_offset = arith.constant(i32, k_step // scale_steps * a_scale_m_stride)
      b_scale_addr_offset = arith.constant(i32, k_step // scale_steps * b_scale_n_stride)
      scales_addrs = (
          arith.addi(a_scale_addr, a_scale_addr_offset),
          arith.addi(b_scale_addr, b_scale_addr_offset),
      )
    elif is_sparse:
      i_desc = create_instr_descriptor(
          m * num_cta, n * num_cta, d_type, element_type, a_transpose, b_transpose, sparsity_selector=sp_selector
      )
    else:
      i_desc = create_instr_descriptor(
          m * num_cta, n * num_cta, d_type, element_type, a_transpose, b_transpose
      )
    if a_in_tmem:
      cols_per_k_group = instr_k // packing // (1 + is_sparse)
      a_offset = k_step * cols_per_k_group
      assert isinstance(a_desc_or_addr, ir.Value)
      assert a_desc_or_addr.type == ir.IntegerType.get_signless(32)
      a_enc_addr_base = a_desc_or_addr
    else:
      assert not isinstance(a_desc_or_addr, ir.Value)
      assert a_k_idx_tiling is not None and a_k_strides is not None
      a_enc_addr_base, a_offset = a_desc_or_addr
      a_offset += _get_offset(k_step, a_k_idx_tiling, a_k_strides)  # pyrefly: ignore[bad-argument-type]
    b_enc_addr_base, b_offset = b_desc
    b_offset += _get_offset(k_step, b_k_idx_tiling, b_k_strides)  # pyrefly: ignore[bad-argument-type]
    a_offset_low, a_offset_high = a_offset & 0xFFFFFFFF, a_offset >> 32
    b_offset_low, b_offset_high = b_offset & 0xFFFFFFFF, b_offset >> 32
    llvm.inline_asm(
        ir.Type.parse("!llvm.void"),
        [d_addr, a_enc_addr_base, b_enc_addr_base, i_desc, accumulate, *scales_addrs, *sparse_addr],
        f"""{{
            .reg .b32 a_desc_low, a_desc_high, b_desc_low, b_desc_high;
            .reg {".b32" if a_in_tmem else ".b64"} a_desc;
            .reg .b64 b_desc;
            add.s32 a_desc_low, $1, {a_offset_low};
            add.s32 b_desc_low, $2, {b_offset_low};
            mov.b64 b_desc, {{b_desc_low, {b_offset_high}}};
            {"mov.b32 a_desc, a_desc_low;" if a_in_tmem else f"mov.b64 a_desc, {{a_desc_low, {a_offset_high}}};"}
            tcgen05.mma{sparse_mod}.cta_group::{num_cta}.kind::{kind} [$0], {a_ptx}, b_desc, {sparse_meta_ptx}$3, {extra_ptx}$4;
        }}""",
        "r,r,r,r,b" + extra_constraints,
        has_side_effects=True,
    )
    accumulate = arith.constant(i1, 1)

