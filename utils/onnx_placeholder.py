
def onnx_placeholder(g: jit_utils.GraphContext, *inputs, **attrs):
    node = g.original_node
    block = g.block
    env = g.env
    values_in_env = g.values_in_env

    return torch._C._jit_onnx_convert_pattern_from_subblock(
        block, node, env, values_in_env
    )

