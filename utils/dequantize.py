
def dequantize(module, param_name, param_value, target_device, dq_param_name, **kwargs):
    from ..integrations.tensor_parallel import shard_and_distribute_module

    model = kwargs.get("model")
    empty_param = kwargs.get("empty_param")
    casting_dtype = kwargs.get("casting_dtype")
    to_contiguous = kwargs.get("to_contiguous")
    rank = kwargs.get("rank")
    device_mesh = kwargs.get("device_mesh")

    for proj in ["gate_up_proj", "down_proj"]:
        if proj in param_name:
            if device_mesh is not None:
                param_value = shard_and_distribute_module(
                    model,
                    param_value,
                    empty_param,
                    dq_param_name,
                    casting_dtype,
                    to_contiguous,
                    rank,
                    device_mesh,
                )
            blocks_attr = f"{proj}_blocks"
            scales_attr = f"{proj}_scales"
            setattr(module, param_name.rsplit(".", 1)[1], param_value)
            if hasattr(module, blocks_attr) and hasattr(module, scales_attr):
                dequantized = convert_moe_packed_tensors(getattr(module, blocks_attr), getattr(module, scales_attr))
                setattr(module, proj, torch.nn.Parameter(dequantized.to(target_device)))
                delattr(module, blocks_attr)
                delattr(module, scales_attr)


def dequantize(g: jit_utils.GraphContext, input):
    return symbolic_helper.dequantize_helper(g, input)[0]


def dequantize(x, dq_dtype, scale):
  return x.astype(dq_dtype) * jnp.broadcast_to(scale.astype(dq_dtype), x.shape)

