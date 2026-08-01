
def _wrap_submodule(mod, path, module_call_specs):
    if not isinstance(mod, torch.nn.Module):
        raise AssertionError(f"expected torch.nn.Module, got {type(mod)}")
    if path == "":
        raise AssertionError("path must not be empty")
    submodule = torch.fx.graph_module._get_attr(mod, path)

    def update_module_call_signatures(path, in_spec, out_spec):
        if path in module_call_specs:
            if module_call_specs[path]["in_spec"] != in_spec:
                raise AssertionError(
                    f"in_spec mismatch for {path}: {module_call_specs[path]['in_spec']} != {in_spec}"
                )
            if module_call_specs[path]["out_spec"] != out_spec:
                raise AssertionError(
                    f"out_spec mismatch for {path}: {module_call_specs[path]['out_spec']} != {out_spec}"
                )
        module_call_specs[path] = {"in_spec": in_spec, "out_spec": out_spec}

    def check_flattened(flat_args):
        for a in flat_args:
            if not (isinstance(a, (torch.Tensor, str, int, float, bool)) or a is None):
                raise AssertionError(
                    f"Only Tensors or scalars are supported as pytree flattened inputs, got: {a}"
                )

    def pre_hook(module, args, kwargs):
        flat_args, in_spec = pytree.tree_flatten((args, kwargs))
        check_flattened(flat_args)
        flat_args = _export_tracepoint(*flat_args, kind="module_call_inputs", path=path)
        args, kwargs = pytree.tree_unflatten(flat_args, in_spec)
        return args, kwargs

    def post_hook(module, args, kwargs, res):
        _, in_spec = pytree.tree_flatten((args, kwargs))
        flat_res, out_spec = pytree.tree_flatten(res)
        check_flattened(flat_res)
        flat_res = _export_tracepoint(*flat_res, kind="module_call_outputs", path=path)
        update_module_call_signatures(path, in_spec, out_spec)
        return pytree.tree_unflatten(flat_res, out_spec)

    pre_handle = submodule.register_forward_pre_hook(pre_hook, with_kwargs=True)
    post_handle = submodule.register_forward_hook(post_hook, with_kwargs=True)
    return pre_handle, post_handle

