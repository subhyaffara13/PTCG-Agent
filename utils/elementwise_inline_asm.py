
def elementwise_inline_asm(result: _Sequence[_ods_ir.Type], asm_string: _Union[str, _ods_ir.StringAttr], constraints: _Union[str, _ods_ir.StringAttr], pure: _Union[bool, _ods_ir.BoolAttr], packed_element: _Union[int, _ods_ir.IntegerAttr], args: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, ElementwiseInlineAsmOp]:
  op = ElementwiseInlineAsmOp(result=result, asm_string=asm_string, constraints=constraints, pure=pure, packed_element=packed_element, args=args, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def elementwise_inline_asm(
    asm: str,
    *,
    args: Sequence[jax.Array],
    constraints: str,
    pack: int,
    result_shape_dtypes: Sequence[jax.ShapeDtypeStruct],
) -> Sequence[jax.Array]:
  """Inline assembly applying an elementwise operation.

  Args:
    asm: The assembly code to run.
    args: The arguments to pass to the assembly code.
    constraints: LLVM inline assembly `constraints
      <https://llvm.org/docs/LangRef.html#inline-asm-constraint-string>`_.
    pack: The number of elements from each argument expected by a single
      instance of the assembly code.
    result_shape_dtypes: The shapes and dtypes of the results produced by the
      assembly code.

  Returns:
    The results produced by the assembly code.
  """
  return elementwise_inline_asm_p.bind(
      *args,
      asm=asm,
      constraints=constraints,
      pack=pack,
      result_shape_dtypes=tuple(result_shape_dtypes),
  )

