
def custom_call(result: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value], call_target_name: _Union[str, _ods_ir.StringAttr], *, has_side_effect: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, backend_config: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, api_version: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, called_computations: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, custom_call_schedule: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, operand_layouts: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, result_layouts: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, output_operand_aliases: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CustomCallOp]:
  op = CustomCallOp(result=result, inputs=inputs, call_target_name=call_target_name, has_side_effect=has_side_effect, backend_config=backend_config, api_version=api_version, called_computations=called_computations, custom_call_schedule=custom_call_schedule, operand_layouts=operand_layouts, result_layouts=result_layouts, output_operand_aliases=output_operand_aliases, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def custom_call(result: _Sequence[_ods_ir.Type], inputs: _Sequence[_ods_ir.Value], call_target_name: _Union[str, _ods_ir.StringAttr], *, has_side_effect: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, backend_config: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, api_version: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, called_computations: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, operand_layouts: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, result_layouts: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, output_operand_aliases: _Optional[_Union[_Any, _ods_ir.ArrayAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _Union[_ods_ir.OpResult, _ods_ir.OpResultList, CustomCallOp]:
  op = CustomCallOp(result=result, inputs=inputs, call_target_name=call_target_name, has_side_effect=has_side_effect, backend_config=backend_config, api_version=api_version, called_computations=called_computations, operand_layouts=operand_layouts, result_layouts=result_layouts, output_operand_aliases=output_operand_aliases, loc=loc, ip=ip); results = op.results
  return results if len(results) > 1 else (results[0] if len(results) == 1 else op)


def custom_call(
    call_target_name: str,
    *,
    result_types: Sequence[ir.Type],
    operands: Sequence[ir.Value],
    backend_config: str | bytes | dict[str, ir.Attribute] = "",
    has_side_effect: bool = False,
    result_shapes: Sequence[ir.Value] | None = None,
    called_computations: Sequence[str] = (),
    api_version: int = 2,
    operand_output_aliases: dict[int, int] | None = None,
    operand_layouts: Sequence[Sequence[int]] | None = None,
    result_layouts: Sequence[Sequence[int]] | None = None,
    extra_attributes: dict[str, ir.Attribute] | None = None,
) -> hlo.CustomCallOp:
  """Helper function for building an hlo.CustomCall.

  Args:
    call_target_name: the name of the custom call target
    result_types: the MLIR types of the results of the custom call
    operands: the MLIR IR values that are arguments to the custom call
    backend_config: an opaque string passed to the custom call kernel
    has_side_effect: if True, marks the custom call as effectful
    result_shapes: tensors that represent the result shapes, to be used when
      the results have dynamic shapes. If not-None, its length must match the
      number of the results.
    called_computations: the list of function names called by the custom call.
    api_version: the ABI contract version of the custom call
    operand_output_aliases: a dict mapping operand numbers to outputs they alias
    operand_layouts: a sequence of layouts (dimension orders) for each operand
    result_layouts: a sequence of layouts (dimension orders) for each result
    extra_attributes: additional IR attributes to apply to the custom_call.
  """
  operands = list(operands)

  if backend_config is None:
    backend_config_attr = ir.StringAttr.get("")
  elif isinstance(backend_config, (str, bytes)):
    backend_config_attr = ir.StringAttr.get(backend_config)
  elif isinstance(backend_config, dict):
    # TODO(necula): it seems that the CustomCallOp constructor requires that
    # backend_config_attr be a string attribute, even though in some cases we
    # need it to be a DictAttr, e.g., for ApproxTopK on TPU.
    # "Verification failed: 'stablehlo.custom_call' op attribute 'backend_config' failed to satisfy constraint: string attribute"
    # To workaround this limitation we first set it to the empty string and we
    # use an unregistered attribute mhlo.backend_config to hold the DictAttr.
    # We must also use api_version=1 to ensure that mhlo.backend_config is
    # handled properly.
    backend_config_attr = ir.StringAttr.get("")
    api_version = 1
  else:
    raise ValueError("custom_call backend_config unexpected type: " + str(backend_config))
  attributes = dict(
      call_target_name=ir.StringAttr.get(call_target_name),
      has_side_effect=ir.BoolAttr.get(has_side_effect),
      backend_config=backend_config_attr,
      api_version=i32_attr(api_version),
      called_computations=ir.ArrayAttr.get(
          [ir.FlatSymbolRefAttr.get(name) for name in called_computations]
      ),
  )
  if operand_output_aliases is not None:
    attributes["output_operand_aliases"] = ir.ArrayAttr.get([
      hlo.OutputOperandAlias.get(
          # if len(result_types) == 1 then the aliasing refers implicitly to
          # the only output.
          output_tuple_indices=[output_idx] if len(result_types) > 1 else [],
          operand_index=input_idx,
          operand_tuple_indices=[],
      )
      for input_idx, output_idx in (operand_output_aliases.items() or ())
    ])

  if extra_attributes is not None:
    attributes.update(extra_attributes)

  if result_shapes is not None:
    # We add the result_shapes at the end of the operands, and must pass
    # the indices_of_output_operands attribute. This attribute is not yet
    # accepted by the CustomCall constructor, so we use build_generic
    attributes["indices_of_shape_operands"] = ir.DenseIntElementsAttr.get(
        np.asarray(list(range(len(operands), len(operands) + len(result_shapes))),
                   dtype=np.int64))
    if operand_layouts is not None:
      assert len(operand_layouts) == len(operands), (operand_layouts, operands)
      operand_layouts = list(operand_layouts) + [(0,)] * len(result_shapes)
    operands = list(operands) + list(result_shapes)

  if operand_layouts is not None:
    attributes["operand_layouts"] = ir.ArrayAttr.get([
        ir.DenseIntElementsAttr.get(
            np.atleast_1d(np.asarray(l, dtype=np.int64)),
            type=ir.IndexType.get()) for l in operand_layouts
    ])
  if result_layouts is not None:
    assert result_layouts is not None
    assert len(result_layouts) == len(result_types), (
        result_layouts, result_types)
    attributes["result_layouts"] = ir.ArrayAttr.get([
        ir.DenseIntElementsAttr.get(
            np.atleast_1d(np.asarray(l, dtype=np.int64)),
            type=ir.IndexType.get()) for l in result_layouts
    ])

  op = hlo.CustomCallOp.build_generic(results=result_types, operands=operands,
                                      attributes=attributes)
  if isinstance(backend_config, dict):
    op.operation.attributes["mhlo.backend_config"] = ir.DictAttr.get(
        backend_config)
  return op

