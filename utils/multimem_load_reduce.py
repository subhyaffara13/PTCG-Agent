
def multimem_load_reduce(source: _ods_ir.Value[_ods_ir.MemRefType], reduction_type: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return MultimemLoadReduceOp(source=source, reduction_type=reduction_type, results=results, loc=loc, ip=ip).result


def multimem_load_reduce(
    ref: _Ref,
    *,
    collective_axes: Hashable | tuple[Hashable, ...],
    reduction_op: mgpu.MultimemReductionOp,
) -> jax.Array:
  """Loads from a GMEM reference on all devices present in collective_axes and reduces the loaded values.

  The supported dtypes are: ``jnp.float32``, ``jnp.float16``, ``jnp.bfloat16``,
  ``jnp.float8_e5m2``, ``jnp.float8_e4m3fn``, ``jnp.int32`` and ``jnp.int64``.

  8-bit floating point dtypes are only supported on Blackwell GPUs.

  Args:
    ref: The GMEM reference to load from.
    collective_axes: The JAX mesh axes indicating the devices to load from.
    reduction_op: The reduction operation to perform on the loaded values. The
      allowed values are add (all dtypes), min, max (all dtypes but f32), as
      well as and, or and xor (integer types only).
  """
  ref, ref_transforms = state_primitives.get_ref_and_transforms(
      ref, None, "multimem_load_reduce"
  )
  flat_ref_transforms, ref_transforms_treedef = tree_util.tree_flatten(
      ref_transforms
  )
  return multimem_load_reduce_p.bind(
      ref,
      *flat_ref_transforms,
      tree=ref_transforms_treedef,
      collective_axes=collective_axes,
      reduction_op=reduction_op,
  )


def multimem_load_reduce(
    ty: ir.Type,
    ptr: ir.Value,
    reduction: MultimemReductionOp,
    is_signed: bool | None = None,
):
  i32 = ir.IntegerType.get_signless(32)
  if bitwidth(ty) not in {32, 64, 128}:
    raise ValueError("Only 32-, 64- and 128-bit loads are supported")
  if isinstance(ty, ir.VectorType):
    vty = ir.VectorType(ty)
    if len(vty.shape) > 1:
      raise ValueError("Only 1D vectors are supported")
    vector_length = vty.shape[0]
    vector_i32_length = vector_length * bitwidth(vty.element_type) // 32
    if isinstance(vty.element_type, ir.IntegerType):
      if vector_length != 1:
        results = []
        elem_ty = vty.element_type
        for i in range(vector_length):
          elem_ptr = getelementptr(ptr, [i], elem_ty)
          v1_ty = ir.VectorType.get((1,), elem_ty)
          elem_res = multimem_load_reduce(
              v1_ty, elem_ptr, reduction, is_signed=is_signed
          )
          results.append(elem_res)
        return vector_concat(results)
      if bitwidth(vty.element_type) not in {32, 64}:
        raise NotImplementedError(
            "Only 32-bit and 64-bit integer operations are supported"
        )
      if reduction in {"and", "or", "xor"}:
        ptx_ty = f"b{bitwidth(vty.element_type)}"
      elif reduction in {"min", "max", "add"}:
        if is_signed is None:
          raise ValueError(
              "Signedness must be specified for integer min, max and add"
              " reductions"
          )
        ptx_ty = f"{'s' if is_signed else 'u'}{bitwidth(vty.element_type)}"
      else:
        raise ValueError(f"Unsupported reduction operation: {reduction}")
    elif isinstance(vty.element_type, ir.FloatType):
      if reduction not in {"add", "min", "max"}:
        raise ValueError("Only add, min and max are supported for floats")
      if isinstance(vty.element_type, ir.F32Type):
        if reduction != "add":
          raise ValueError("Only add is supported for f32")
        ptx_ty = "f32"
      elif isinstance(vty.element_type, ir.BF16Type):
        ptx_ty = "bf16x2"
      elif isinstance(vty.element_type, ir.F16Type):
        ptx_ty = "f16x2"
      elif isinstance(vty.element_type, ir.Float8E5M2Type):
        ptx_ty = "e5m2x4"
      elif isinstance(vty.element_type, ir.Float8E4M3FNType):
        ptx_ty = "e4m3x4"
      else:
        raise NotImplementedError(vty.element_type)
    else:
      raise NotImplementedError(vty.element_type)
  else:
    raise NotImplementedError(ty)
  if vector_i32_length == 1:
    vec_ptx = "$0"
    vec_mod = ""
  else:
    vec_ptx = f"{{{','.join(f'${i}' for i in range(vector_i32_length))}}}"
    vec_mod = ".v" + str(vector_i32_length)
  # It's unclear to me why, but at least according to PTX docs, we have to use
  # the floating-point instructions here to be able to store vectors.
  acc_prec = ""
  if vector_i32_length == 1:
    asm_out_ty = i32
  else:
    asm_out_ty = llvm.StructType.get_literal([i32] * vector_i32_length)
  out_reg_struct = llvm.inline_asm(
      asm_out_ty,
      [ptr],
      f"multimem.ld_reduce.relaxed.sys.global.{reduction}{acc_prec}{vec_mod}.{ptx_ty}"
      f" {vec_ptx}, [${vector_i32_length}];",
      "=r," * vector_i32_length + "l",
      has_side_effects=True,
  )
  assert isinstance(out_reg_struct, ir.Value)
  if vector_i32_length == 1:
    return bitcast(out_reg_struct, ty)
  else:
    out_regs = [
        llvm.extractvalue(i32, out_reg_struct, [i])
        for i in range(vector_i32_length)
    ]
    vec_i32_ty = ir.VectorType.get((1,), i32)
    return bitcast(
        vector_concat([bitcast(out_reg, vec_i32_ty) for out_reg in out_regs]),
        ty,
    )

