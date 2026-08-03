import itertools
import math


def wgmma_m64(
    acc: np.ndarray,  # of register Values
    a,
    b_descriptor: ir.Value,
    a_transpose: bool | None,
    b_transpose: bool,
    a_k_stride: int | None,
    b_k_stride: int,
    n: int,
    swizzle: int,
    element_type: ir.Type,
):
  out_ty = ir.VectorType(acc.flat[0].type).element_type
  if not _supported_wgmma_types(out_ty, element_type):
    raise ValueError(f"Unsupported wgmma types {(out_ty, element_type)=}")
  if n % 8:
    raise ValueError

  bf16 = ir.BF16Type.get()
  f16 = ir.F16Type.get()
  i8 = ir.IntegerType.get_signless(8)
  i32 = ir.IntegerType.get_signless(32)
  i64 = ir.IntegerType.get_signless(64)
  f8e5m2 = ir.Float8E5M2Type.get()
  f8e4m3fn = ir.Float8E4M3FNType.get()
  if b_k_stride % 16:
    raise ValueError
  # Only 16-bit types support transposes
  supports_transpose = bytewidth(element_type) == 2
  if not supports_transpose and (a_transpose or b_transpose):
    raise ValueError("Only f16 WGMMA supports transposes")
  if a_in_regs := isinstance(a, fa.FragmentedArray):
    if a.mlir_dtype not in {bf16, f16, i8, f8e5m2, f8e4m3fn}:
      raise ValueError(f"Unsupported A register array dtype: {a.mlir_dtype}")
    # Column count must be equal to swizzle // bytewidth.
    elt_bytewidth = utils.bytewidth(element_type)
    swizzle_elems = swizzle // elt_bytewidth
    if a.shape != (64, swizzle_elems):
      raise ValueError("Unsupported A register array shape")
    if a.layout not in {fa.WGMMA_LAYOUT, fa.WGMMA_LAYOUT_8BIT}:
      raise ValueError("Unsupported A register array layout")
    if a_k_stride is not None or a_transpose is not None:
      raise ValueError("Unsupported WGMMA features with A in registers")
  else:
    if a_k_stride is None or a_k_stride % 16:
      raise ValueError
    if a_transpose is None:
      raise ValueError

  if isinstance(out_ty, ir.F32Type) or out_ty == i32:
    num_acc_regs = n // 2
    out_ty_field = ir.VectorType.get((1,), out_ty)
    acc_regs = list(acc.flat)
    assert acc_regs[0].type == ir.VectorType.get((1,), out_ty)
    to_acc_vec_regs = lambda regs: np.array(regs).reshape(acc.shape)
    acc_constraint = "r" if isinstance(out_ty, ir.IntegerType) else "f"
  elif isinstance(out_ty, ir.F16Type):
    num_acc_regs = n // 4
    out_ty_field = i32
    acc_regs = [_as_i32_reg(reg) for reg in acc.flat]
    vec_ty = ir.VectorType(acc.flat[0].type)
    to_acc_vec_regs = lambda regs: np.array([_unpack_i32(vec_ty, reg) for reg in regs]).reshape(acc.shape)
    acc_constraint = "r"
  else:
    raise ValueError(
        f"WGMMA instruction only supports f32, f16 and s32 out (got {out_ty})")

  if supports_transpose:
    num_imm_regs = 4
  elif out_ty == i32:
    num_imm_regs = 0
  else:
    num_imm_regs = 2

  if a_in_regs:
    a_reg_constraints = ["r"] * 4  # 4x (b)f16x2 or s8x4 registers
    if supports_transpose:
      num_imm_regs -= 1  # transpose not supported for a in registers
  else:
    a_reg_constraints = ["l"]  # descriptor
  # Reference for i/o aliasing: https://gcc.gnu.org/onlinedocs/gcc/Extended-Asm.html
  # Seems like it's not actually documented in LLVM IR docs.
  reg_constraints_list = (
      [f"={acc_constraint}"] * num_acc_regs  # accumulator registers
      + [str(i) for i in range(num_acc_regs)]  # we alias outputs as inputs, too.
      + a_reg_constraints  # a descriptor / registers
      + ["l"] * 1  # b descriptor
      + ["n"] * (1 + num_imm_regs)  # literal constants
  )
  reg_constraints = ",".join(reg_constraints_list)
  reg_count = itertools.count()

  def take_regs(n):
    return (f"${i}" for i in itertools.islice(reg_count, n))

  acc_reg_vector = "{" + ",".join(take_regs(num_acc_regs)) + "}"
  for _ in take_regs(num_acc_regs):  # Ignore next entries: aliasing.
    pass
  if a_in_regs:
    a_regs = "{" + ",".join(take_regs(len(a_reg_constraints))) + "}"
  else:
    a_regs, = take_regs(1)
  b_desc_reg, use_out_reg = take_regs(2)
  # Immediate regs (scale, ...).
  imm_regs = "".join(f", {r}" for r in take_regs(num_imm_regs))
  assert next(reg_count) == len(reg_constraints_list)
  k_instr = 32 // bytewidth(element_type)
  el_ty = str(element_type)
  if isinstance(element_type, ir.Float8E5M2Type):
    el_ty = "e5m2"
  elif isinstance(element_type, ir.Float8E4M3FNType):
    el_ty = "e4m3"
  elif isinstance(element_type, ir.IntegerType):
    # TODO(bchetioui): add u8 support in the future. Currently we always assume
    # that 8-bit integers are s8, and we would need to change the signature of
    # `wgmma` to indicate whether the input should be treated as signed or not.
    el_ty = "s8"

  out_ty_str = str(out_ty)
  if out_ty == i32:
    out_ty_str = "s32"

  wgmma_instr = (
      f"wgmma.mma_async.sync.aligned.m64n{n}k{k_instr}.{out_ty_str}.{el_ty}.{el_ty} "
      f"{acc_reg_vector}, {a_regs}, {b_desc_reg}, p{imm_regs};"
  )
  ptx = f"{{ .reg .pred p; setp.ne.b32 p, {use_out_reg}, 0; {wgmma_instr} }}\n"

  def lc(x):
    return llvm.ConstantOp(i32, ir.IntegerAttr.get(i32, x)).result

  use_out = scale_a = scale_b = lc(1)
  if out_ty == i32:
    imms = [use_out]
  else:
    imms = [use_out, scale_a, scale_b]

  if supports_transpose and a_transpose is not None:
    imms += [lc(int(a_transpose)), lc(int(b_transpose))]
  elif supports_transpose:
    imms += [lc(int(b_transpose))]

  assert len(imms) == num_imm_regs + 1  # +1 for the use_out_reg in setp.ne.b32

  expected_dim = 10 if utils.bitwidth(out_ty) == 32 else 9
  expected_regs_per_tile = 4 if utils.bitwidth(out_ty) == 32 else 2
  if acc.ndim != expected_dim or acc.shape[0] != 1 or math.prod(acc.shape[2:]) != expected_regs_per_tile:
    raise ValueError(acc.shape)
  for i in range((swizzle // bytewidth(element_type)) // k_instr):
    # Slice out the relevant part of A or advance the A descriptor.
    if a_in_regs:
      a_slice = a[:, (i * k_instr) : ((i + 1) * k_instr)]
      a_args = [_as_i32_reg(v) for v in a_slice.registers.flat]
    else:
      if i > 0:
        assert a_k_stride is not None
        a = _llvm_add(
            a,
            llvm.ConstantOp(i64, ir.IntegerAttr.get(i64, a_k_stride >> 4)),
        )
      a_args = [a]
    # Advance the B descriptor.
    if i > 0:
      b_descriptor = _llvm_add(
          b_descriptor,
          llvm.ConstantOp(i64, ir.IntegerAttr.get(i64, b_k_stride >> 4)),
      )
    assert len(a_args) == len(a_reg_constraints)
    acc_struct = llvm.inline_asm(
        llvm.StructType.get_literal([out_ty_field] * len(acc_regs)),
        [*acc_regs, *a_args, b_descriptor, *imms],
        ptx,
        reg_constraints,
        asm_dialect=0,
        has_side_effects=True,
    )
    assert isinstance(acc_struct, ir.Value)
    acc_regs = [
        llvm.extractvalue(out_ty_field, acc_struct, [i]) for i in range(len(acc_regs))
    ]
  return to_acc_vec_regs(acc_regs)

