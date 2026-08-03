import itertools
from typing import Any, Callable

def _find_mgpu_call(block: ir.Block, args: list[ir.Value]):
  import torch  # pyrefly: ignore[missing-import]
  mgpu_call: hlo.CustomCallOp | None = None
  get_outputs = None
  to_evaluate: list[Callable] = []
  init_env = {}
  name_source = itertools.count()
  value_names: Mapping[ir.Value, int] = defaultdict(lambda: next(name_source))
  for op in block.operations:
    op = cast(Any, op)
    if _is_custom_call(op, "AllocateBuffer"):
      result_type = ir.ShapedType(op.result.type)
      def allocate_torch_buffer(
          env,
          device,
          _shape=result_type.shape,
          _dtype=_mlir_to_torch_dtype(torch, result_type.element_type),
          _result_name=value_names[op.result],
      ):
        env[_result_name] = torch.empty(_shape, dtype=_dtype, device=device)
      to_evaluate.append(allocate_torch_buffer)
    elif _is_custom_call(op, "mosaic_gpu_v2"):
      if mgpu_call is not None:
        raise ValueError("Multiple Mosaic GPU kernels found in the module")
      mgpu_call = op
    elif op.name == "func.return" or op.name == "sdy.return":
      if mgpu_call is None:
        raise ValueError("No Mosaic GPU call found in the module")
      if get_outputs is not None:
        raise ValueError("Multiple return ops found in the module")
      mgpu_results = list(mgpu_call.results)
      try:
        out_indices = [mgpu_results.index(o) for o in op.operands]
      except ValueError:
        raise ValueError("The function can only return kernel results") from None
      def get_outputs(*results, _out_indices=out_indices):
        return tuple(results[i] for i in _out_indices)
    elif op.name == "stablehlo.constant":
      result_type = ir.ShapedType(op.result.type)
      if result_type.shape:
        raise ValueError(f"Only scalar constants are supported, got {op}")
      if not op.value.is_splat:
        raise ValueError(f"Only splat constants are supported, got {op}")
      if result_type.element_type == ir.IntegerType.get_signless(32):
        init_env[value_names[op.result]] = ir.IntegerAttr(
            op.value.get_splat_value()
        ).value
      else:
        raise NotImplementedError(f"Only i32 constants are supported, got {op}")
    elif op.name == "stablehlo.broadcast_in_dim":
      if op.broadcast_dimensions:
        raise ValueError("Only scalar broadcasts are supported")
      result_type = ir.ShapedType(op.result.type)
      target_shape = tuple(result_type.shape)
      result_name = value_names[op.result]
      operand_name = value_names[op.operand]
      dtype = torch.int32
      def run_broadcast(
          env,
          device,
          _target_shape=target_shape,
          _dtype=dtype,
          _operand_name=operand_name,
          _result_name=result_name,
      ):
        env[_result_name] = torch.broadcast_to(
            torch.as_tensor(env[_operand_name], dtype=_dtype, device=device),
            _target_shape,
        )

      to_evaluate.append(run_broadcast)
    else:
      raise ValueError(f"Unsupported operation found in the kernel module: {op}")
  if mgpu_call is None:
    raise ValueError("No Mosaic GPU call found in the module")
  if get_outputs is None:
    raise ValueError("No return op found in the module")

  block_arg_names = [value_names[arg] for arg in block.arguments]
  mgpu_arg_names = [value_names[arg] for arg in mgpu_call.operands]
  def prepare_args(*user_args, device):
    env = dict(init_env)
    for name, arg in zip(block_arg_names, user_args, strict=True):
      env[name] = arg
    for thunk in to_evaluate:
      thunk(env, device)
    return tuple(env[name] for name in mgpu_arg_names)
  output_input_aliases: list[int | None] = [None] * len(mgpu_call.results)
  for alias in mgpu_call.output_operand_aliases or []:
    alias = hlo.OutputOperandAlias(alias)
    if alias.operand_tuple_indices:
      raise NotImplementedError("Tupled operand indices not supported")
    if len(alias.output_tuple_indices) > 1:
      raise NotImplementedError("Expected one element in output_tuple_indices")
    [output_index] = alias.output_tuple_indices or (0,)
    output_input_aliases[output_index] = alias.operand_index

  output_types = [
      (result_type.shape, _mlir_to_torch_dtype(torch, result_type.element_type))
      for result in mgpu_call.results
      if isinstance(result_type := result.type, ir.ShapedType)
  ]
  def prepare_outputs(*all_args, device):
    outputs = []
    for ty, alias in zip(output_types, output_input_aliases, strict=True):
      if alias is not None:
        outputs.append(all_args[alias])
        continue
      outputs.append(torch.empty(ty[0], dtype=ty[1], device=device))
    return outputs

  return mgpu_call, prepare_args, prepare_outputs, get_outputs

