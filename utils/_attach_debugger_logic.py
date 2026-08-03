import functools
import os

def _attach_debugger_logic(
    model,
    debug_path: str = ".",
    do_prune_layers: bool = True,
    use_repr: bool = True,
):
    """
    Attaches a debugging wrapper to every module in the model.

    This records structured inputs and outputs during the forward pass into a call tree.

    Args:
        model (`PreTrainedModel`, `nn.Module`): Model to wrap.
        debug_path (`str`): Optional directory to dump debug JSON files.
        do_prune_layers (`bool`, *optional*, defaults to `True`): Whether to prune intermediate layers.
        use_repr (bool, *optional*, defaults to `True`): Whether to save a `repr()`-ized version of the tensors as the
            `value` property in the associated FULL_TENSORS.json file, or to store full tensors in separate SafeTensors
            files and store the relative path to that file in the `value` property.
    """
    class_name = model.__class__.__name__

    # Prepare data structures on the model object
    model._call_tree = {"module_path": class_name, "inputs": None, "outputs": None, "children": []}
    model._debugger_model_call_stack = []
    model._debugger_module_dump_name = class_name  # used for final JSON filename

    if debug_path:
        try:
            os.makedirs(debug_path, exist_ok=True)
        except Exception as e:
            raise ValueError(f"Unexpected or existing debug_path={debug_path}.") from e

    def wrap_forward(module, full_path):
        orig_forward = module.forward

        @functools.wraps(orig_forward)
        def wrapped_forward(*inps, **kws):
            if _is_rank_zero():
                dict_inputs = {"args": inps, "kwargs": kws}
                dict_inputs = {k: dict_inputs[k] for k in dict_inputs if len(dict_inputs[k]) > 0}
                node = {
                    "module_path": full_path,
                    "inputs": _serialize_io(
                        dict_inputs,
                        debug_path=debug_path,
                        use_repr=use_repr,
                        path_to_value=f"{full_path}_inputs",
                    ),
                    "outputs": None,
                    "children": [],
                }
                model._debugger_model_call_stack.append(node)
            with torch.no_grad():
                out = orig_forward(*inps, **kws)

            if _is_rank_zero():
                if sum(1 for _ in module.named_children()) > 0:
                    node["outputs"] = None
                else:
                    node["outputs"] = _serialize_io(
                        out,
                        debug_path=debug_path,
                        use_repr=use_repr,
                        path_to_value=f"{full_path}_outputs",
                    )

                finished = model._debugger_model_call_stack.pop()
                # prune empty vertices here as well (mostly empty children nodes)
                if not finished["children"]:
                    finished.pop("children")

                if model._debugger_model_call_stack:
                    model._debugger_model_call_stack[-1]["children"].append(finished)
            return out

        module.forward = wrapped_forward

    # wrap all submodules
    for name, submodule in model.named_modules():
        if name == "":
            continue
        wrap_forward(submodule, f"{class_name}.{name}")

    # wrap top-level forward
    real_top_forward = model.forward

    @functools.wraps(real_top_forward)
    def top_wrapped_forward(*inps, **kws):
        if _is_rank_zero():
            top_node = {
                "module_path": f"{class_name} (top-level)",
                "inputs": _serialize_io(
                    {"args": inps, "kwargs": kws},
                    debug_path=debug_path,
                    use_repr=use_repr,
                    path_to_value=f"{class_name}_inputs",
                ),
                "outputs": None,
                "children": [],
            }
            model._debugger_model_call_stack.append(top_node)

        out = real_top_forward(*inps, **kws)
        if _is_rank_zero() and model._debugger_model_call_stack:
            top_node["outputs"] = _serialize_io(
                out,
                debug_path=debug_path,
                use_repr=use_repr,
                path_to_value=f"{class_name}_outputs",
            )
            finished = model._debugger_model_call_stack.pop()
            model._call_tree["inputs"] = finished["inputs"]
            model._call_tree["outputs"] = finished["outputs"]
            model._call_tree["children"] = finished["children"]
            # prune empty stuff for visibility
            [model._call_tree.pop(k, None) for k in list(model._call_tree.keys()) if not model._call_tree[k]]

            # prune layers that are not 0 or last
            if do_prune_layers:
                prune_intermediate_layers(model._call_tree)
            # Write final JSON trace here
            log_model_debug_trace(debug_path=debug_path, model=model)
        return out

    model.forward = top_wrapped_forward

