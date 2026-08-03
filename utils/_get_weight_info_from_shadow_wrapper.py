from typing import Any

def _get_weight_info_from_shadow_wrapper(shadow_wrapper: torch.nn.Module):
    # input: shadow wrapper module
    # output if shadow wrapper module has a weighted op:
    #   (quantize_fn, (quantize_fn_args))
    # output if shadow wrapper module doesn't have a weighted op:
    #   None

    # For now, assume that the weight is the second input
    # to the shadow module. If that changes, we can fix it later.
    placeholders_seen = 0
    for shadow_n in shadow_wrapper.graph.nodes:  # type: ignore[union-attr]
        if shadow_n.op != "placeholder":
            continue

        placeholders_seen += 1
        if placeholders_seen != 2:
            continue

        # the subgraph looks like
        #
        #   _input_scale_1 = self._input_scale_1
        #   _input_zero_point_1 = self._input_zero_point_1
        #   quantize_per_channel = torch.quantize_per_channel(
        #       w2_0, _input_scale_1, _input_zero_point_1,
        #       0, torch.qint8)
        #
        #  we have `w2_0`, and are navigating this subgraph
        #  to get `_input_scale_1` and `_input_zero_point_1`

        if len(shadow_n.users) != 1:
            raise AssertionError(f"Expected exactly 1, got {len(shadow_n.users)}")
        quant_node = next(iter(shadow_n.users.keys()))
        new_args: Any = None
        if quant_node.target is torch.quantize_per_channel:
            _weight, scale_node, zp_node, axis, dtype = quant_node.args
            scale_val = getattr_from_fqn(shadow_wrapper, scale_node.target)
            zp_val = getattr_from_fqn(shadow_wrapper, zp_node.target)
            new_args = (scale_val, zp_val, axis, dtype)
        else:
            if quant_node.target != torch.quantize_per_tensor:
                raise AssertionError(
                    f"Expected torch.quantize_per_tensor, but got {quant_node.target}"
                )
            _weight, scale_node, zp_node, dtype = quant_node.args
            scale_val = getattr_from_fqn(shadow_wrapper, scale_node.target)
            zp_val = getattr_from_fqn(shadow_wrapper, zp_node.target)
            new_args = (scale_val, zp_val, dtype)
        return (quant_node.target, new_args)

    return None

