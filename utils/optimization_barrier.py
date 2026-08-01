
def optimization_barrier(operands_: _Sequence[_ods_ir.Value], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, OptimizationBarrierOp]:
  op = OptimizationBarrierOp(operands_=operands_, results=results, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def optimization_barrier(operand: _Sequence[_ods_ir.Value], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, OptimizationBarrierOp]:
  op = OptimizationBarrierOp(operand=operand, results=results, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def optimization_barrier(operand: _Sequence[_ods_ir.Value], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, OptimizationBarrierOp]:
  op = OptimizationBarrierOp(operand=operand, results=results, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def optimization_barrier(operand, /):
  """Prevents the compiler from moving operations across the barrier.

  Optimization barriers have a number of possible uses:

  * An optimization barrier ensures that every output of the barrier that is
    used by any operator, has been evaluated before any operator that depends
    on one of the barrier's outputs. This can be used to enforce a particular
    order of operations.

    Note that all operands must be used through the barrier for this to work.
    There are no ordering constraints between an operator that uses one of the
    barrier's outputs, and an operator that directly (not through the barrier)
    uses one of the barrier's inputs.
  * An optimization barrier prevents common subexpression elimination. This is
    used by JAX to implement rematerialization.
  * Optimization barriers prevent compiler fusions. That is, operations before
    the barrier may not be fused into the same kernel as operations after the
    barrier by the compiler.

  JAX does not define derivative or batching rules for an optimization barrier.

  Optimization barriers have no effect outside a compiled function.

  Args:
    operand: a pytree of JAX values.

  Returns:
    A pytree of JAX values, with the same structure and contents as ``operand``.

  Examples:
    Prevents common-subexpression elimination between the two calls to `sin`:

    >>> def f(x):
    ...   return jax.lax.optimization_barrier(jax.lax.sin(x)) + jax.lax.sin(x)
    >>> jax.jit(f)(0.)
    Array(0., dtype=float32, weak_type=True)
  """
  flat_args, treedef = tree_util.tree_flatten(operand)
  flat_args = core.auto_insert_reshard(*flat_args)
  out = optimization_barrier_p.bind(*flat_args)
  return tree_util.tree_unflatten(treedef, out)


def optimization_barrier(
    a: mgpu.FragmentedArray,
    b: mgpu.FragmentedArray,
    /,
    *arrays: mgpu.FragmentedArray,
) -> Sequence[mgpu.FragmentedArray]:
  ...


def optimization_barrier(a: mgpu.FragmentedArray, /) -> mgpu.FragmentedArray:
  ...


def optimization_barrier(*arrays):
  """Acts as an optimization barrier for LLVM.

  Passing arrays through this function will make sure that they are computed
  before any side-effecting operations that follow this barrier.
  """
  i32 = ir.IntegerType.get_signless(32)

  def _repack(regs_it, reg_ty):
    if not isinstance(reg_ty, ir.VectorType):
      result_reg = next(regs_it)
      assert result_reg.type == reg_ty
      return result_reg

    num_i32_regs = utils.bitwidth(reg_ty) // 32
    i32_reg_ty = ir.VectorType.get((num_i32_regs,), i32)
    reg = llvm.mlir_undef(i32_reg_ty)
    for i_elem in range(num_i32_regs):
      val = llvm.bitcast(i32, next(regs_it))
      reg = llvm.insertelement(reg, val, arith.constant(i32, i_elem))
    return vector.bitcast(reg_ty, reg)

  regs = []
  reg_dtypes = []
  reg_constraints = []
  # We unpack each array into a flat list of registers, and prepare the
  # functions that invert the transform in repack_fns.
  for array in arrays:
    reg_ty = array.registers.flat[0].type
    dtype = array.mlir_dtype
    if isinstance(dtype, ir.F32Type) or dtype == i32:
      if isinstance(reg_ty, ir.VectorType):
        [vec_len] = ir.VectorType(reg_ty).shape
        array_regs = [
            vector.extract(
                reg,
                dynamic_position=[],
                static_position=ir.DenseI64ArrayAttr.get([pos]),
            )
            for reg in array.registers.flat
            for pos in range(vec_len)
        ]
      else:
        array_regs = list(array.registers.flat)
      reg_constraint = "r" if dtype == i32 else "f"
    elif utils.bitwidth(dtype) < 32:
      reg_packing = 4 // utils.bytewidth(dtype)
      if not isinstance(reg_ty, ir.VectorType):
        raise NotImplementedError(array.mlir_dtype)
      [vec_len] = ir.VectorType(reg_ty).shape
      if vec_len % reg_packing:
        raise NotImplementedError(vec_len)
      num_i32_regs = vec_len // reg_packing
      i32_reg_ty = ir.VectorType.get((num_i32_regs,), i32)
      array_regs = [
          vector.extract(
              vector.bitcast(i32_reg_ty, reg),
              dynamic_position=[],
              static_position=ir.DenseI64ArrayAttr.get([i]),
          )
          for i in range(num_i32_regs)
          for reg in array.registers.flat
      ]
      reg_constraint = "r"
    else:
      raise NotImplementedError(array.mlir_dtype)
    regs += array_regs
    reg_dtypes += [array_regs[0].type] * len(array_regs)
    reg_constraints += [reg_constraint] * len(array_regs)
  ptx = ""
  all_reg_constraints = ",".join(
      [*("=" + c for c in reg_constraints), *map(str, range(len(reg_constraints)))]
  )

  if len(reg_dtypes) == 1:
    # The InlineAsm::verify() function doesn't allow a struct output when there
    # is only one element (even though that seems to work for the case below).
    result_elem = llvm.inline_asm(
        reg_dtypes[0], regs, ptx, all_reg_constraints,
        asm_dialect=0, has_side_effects=True,
    )
    regs = [result_elem]
  else:
    struct_ty = llvm.StructType.get_literal(reg_dtypes)
    result_struct = llvm.inline_asm(
        struct_ty, regs, ptx, all_reg_constraints,
        asm_dialect=0, has_side_effects=True,
    )
    assert isinstance(result_struct, ir.Value)
    regs = [
        llvm.extractvalue(dtype, result_struct, [i])
        for i, dtype in enumerate(reg_dtypes)
    ]

  i32 = ir.IntegerType.get_signless(32)
  results = []
  regs_it = iter(regs)
  for array in arrays:
    num_regs = array.registers.size
    reg_ty = array.registers.flat[0].type
    if isinstance(reg_ty, ir.VectorType):
      reg_ty = ir.VectorType(reg_ty)
    new_registers = np.empty((num_regs,), dtype=object)
    for i_vreg in range(num_regs):
      reg = _repack(regs_it, reg_ty)
      assert reg.type == reg_ty, (reg.type, reg_ty)
      new_registers[i_vreg] = reg
    results.append(
        FragmentedArray(
            _registers=new_registers.reshape(array.registers.shape),
                        _layout=array.layout,
            _is_signed=array.is_signed,
        )
    )
  return results[0] if len(arrays) == 1 else results

