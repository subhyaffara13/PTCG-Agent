import functools
import itertools

def _wrap_main_func(
    module: ir.Module,
    args_avals_flat: Sequence[core.ShapedArray],
    *,
    args_kwargs_tree: tree_util.PyTreeDef,
    has_platform_index_argument: bool,
    module_kept_var_idx: tuple[int, ...],
    serialization_version: int
) -> ir.Module:
  """Wraps the lowered module with a new "main" handling dimension arguments.

  See calling convention documentation https://docs.jax.dev/en/latest/export/export.html#module-calling-convention.

  Args:
    module: a copy of HLO module as obtained from lowering.
    args_avals_flat: the avals for all the arguments of the lowered function,
      which correspond to the array arguments of the ``module``.
    args_kwargs_tree: the PyTreeDef corresponding to ``(args, kwargs)``, for error
      messages.
    has_platform_index_argument: whether the ``module`` has a first platform
      index argument
    module_kept_var_idx: a sorted tuple of integers with the indices of arguments
      in ``args_avals_flat`` that are kept as ``module`` arguments.
    serialization_version: the target serialization version

  Returns the wrapped module, without dimension and token arguments.
  """
  dim_vars = shape_poly.all_dim_vars(args_avals_flat)
  context = module.context
  wrapped_module = module
  with context, ir.Location.unknown(context):
    symbol_table = ir.SymbolTable(wrapped_module.operation)
    orig_main = cast(func_dialect.FuncOp, symbol_table["main"])
    orig_main.attributes["sym_visibility"] = ir.StringAttr.get("private")
    symbol_table.set_symbol_name(orig_main, "_wrapped_jax_export_main")
    orig_main_name = ir.StringAttr(symbol_table.insert(orig_main)).value

    def is_token(typ, attrs):
      return (typ == mlir.token_type())

    orig_input_types = orig_main.type.inputs
    arg_attrs = list(ir.ArrayAttr(orig_main.arg_attrs))
    # The order of args: platform_index_arg, dim args, token args, array args.
    nr_platform_index_args = 1 if has_platform_index_argument else 0
    nr_dim_args = len(dim_vars)
    token_arg_idxs = [i for i, (typ, attrs) in enumerate(zip(orig_input_types,
                                                             arg_attrs))
                      if is_token(typ, attrs)]
    nr_token_args = len(token_arg_idxs)
    if nr_token_args > 0:
      assert min(token_arg_idxs) == nr_platform_index_args + nr_dim_args
      assert token_arg_idxs == list(
        range(nr_platform_index_args + nr_dim_args,
              nr_platform_index_args + nr_dim_args + nr_token_args))
    nr_array_args = (len(orig_input_types) - nr_platform_index_args
                     - nr_dim_args - nr_token_args)
    assert nr_array_args >= 0

    (platform_input_types, dim_var_input_types,
     token_input_types, array_input_types) = util.split_list(
      orig_input_types, [nr_platform_index_args, nr_dim_args, nr_token_args])

    # The order of results: tokens, array results
    orig_output_types = orig_main.type.results
    result_attrs = list(ir.ArrayAttr(orig_main.result_attrs))
    token_result_idxs = [i for i, (typ, attrs) in enumerate(zip(orig_output_types,
                                                                result_attrs))
                         if is_token(typ, attrs)]
    nr_token_results = len(token_result_idxs)
    assert token_result_idxs == list(range(0, nr_token_results))
    nr_array_results = len(orig_output_types) - nr_token_results
    assert nr_array_results >= 0
    new_main_arg_indices = (
        *range(nr_platform_index_args),
        *range(nr_platform_index_args + nr_dim_args, len(orig_input_types)))
    new_main_result_indices = tuple(range(0, len(orig_output_types)))

    new_main_input_types = [orig_input_types[idx] for idx in new_main_arg_indices]
    new_main_output_types = [orig_output_types[idx] for idx in new_main_result_indices]
    new_main_ftype = ir.FunctionType.get(new_main_input_types, new_main_output_types)
    new_main_op = func_dialect.FuncOp(
        "main", new_main_ftype, ip=ir.InsertionPoint.at_block_begin(wrapped_module.body))
    new_main_op.attributes["sym_visibility"] = ir.StringAttr.get("public")
    try:
      new_arg_attrs = []
      for idx in new_main_arg_indices:
        new_arg_attr: dict[str, ir.Attribute] = {}
        for attr in arg_attrs[idx]:  # pyrefly: ignore[not-iterable]
          if attr.name == "tf.aliasing_output":
            i = new_main_result_indices.index(attr.attr.value)
            new_arg_attr[attr.name] = ir.IntegerAttr.get(
                ir.IntegerType.get_signless(32), i
            )
          else:
            new_arg_attr[attr.name] = attr.attr
        new_arg_attrs.append(ir.DictAttr.get(new_arg_attr))
      new_main_op.arg_attrs = ir.ArrayAttr.get(new_arg_attrs)
    except KeyError:
      pass  # TODO: better detection if orig_main.arg_attrs does not exist
    try:
      new_main_op.result_attrs = ir.ArrayAttr.get(
          [result_attrs[idx] for idx in new_main_result_indices])
    except KeyError:
      pass
    symbol_table.insert(new_main_op)
    entry_block = new_main_op.add_entry_block()
    with ir.InsertionPoint(entry_block):
      # Make a context just for lowering the dimension value computations
      module_context = mlir.ModuleContext(
          backend=None, platforms=["cpu"],
          axis_context=sharding_impls.ShardingContext(0),
          keepalives=[], channel_iterator=itertools.count(1),
          host_callbacks=[], module=wrapped_module, context=context,
          lowering_parameters=mlir.LoweringParameters(
              global_constant_computation=True,
              for_export=True, hoist_constants_as_args=False,
              export_ignore_forward_compatibility=config.export_ignore_forward_compatibility.value,
          ))
      ctx = mlir.LoweringRuleContext(
        module_context=module_context,
        name_stack=source_info_util.new_name_stack(), traceback=None,
        primitive=None,
        avals_in=args_avals_flat, avals_out=None,
        tokens_in=mlir.TokenSet(), tokens_out=None,
        const_lowering={})
      # We compute dim_values from the array arguments.
      new_main_op_array_args = new_main_op.arguments[-nr_array_args:]
      if shape_poly.all_dim_vars(args_avals_flat):
        # TODO(necula): handle module_kept_var_idx in presence of shape
        # polymorphism. For now we ensured upstream that we keep all variables.
        assert len(set(module_kept_var_idx)) == len(args_avals_flat)
        dim_values = mlir.lower_fun(
            functools.partial(shape_poly.compute_dim_vars_from_arg_shapes,
                              args_avals_flat, args_kwargs_tree=args_kwargs_tree),
            multiple_results=True)(ctx, *new_main_op_array_args)
      else:
        dim_values = ()
      flat_dim_values, _ = mlir.ir_tree_registry.flatten(dim_values)
      # The arguments to pass to the call to orig_main
      orig_main_args: list[ir.Value] = []
      # The platform index and the dimension variables
      for arg, arg_type in zip(
          list(new_main_op.arguments[0:nr_platform_index_args]) + flat_dim_values,
          platform_input_types + dim_var_input_types):
        if arg.type != arg_type:
          orig_main_args.append(hlo.convert(arg_type, arg))
        else:
          orig_main_args.append(arg)
      # Then the token arguments
      orig_main_args.extend(
        new_main_op.arguments[nr_platform_index_args: nr_platform_index_args + nr_token_args])
      # Then the array arguments. We insert a ConvertOp as the only use of
      # an input argument. This helps the downstream shape refinement because
      # it will set the type of input arguments to static shapes, and this
      # can invalidate the module if the argument is used as the result of a
      # function, or if it appears as the input to a custom_call with
      # output_operand_alias attribute. See b/287386268.
      for arg, arg_type in zip(new_main_op_array_args, array_input_types):
        if arg.type != arg_type:
          orig_main_args.append(hlo.convert(arg_type, arg))
        else:
          orig_main_args.append(arg)
      call = func_dialect.CallOp(orig_output_types,
                                 ir.FlatSymbolRefAttr.get(orig_main_name),
                                 orig_main_args)
      func_dialect.ReturnOp([call.results[idx] for idx in new_main_result_indices])
    symbol_table.set_symbol_name(new_main_op, "main")
    pipeline = passmanager.PassManager.parse(
        'builtin.module(symbol-dce)')
    pipeline.run(wrapped_module.operation)

  return wrapped_module

