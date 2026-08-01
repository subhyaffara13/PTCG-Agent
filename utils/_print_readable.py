
def _print_readable(
    module,
    module_name,
    print_output=True,
    include_stride=False,
    include_device=False,
    colored=False,
    expanded_def=False,
    additional_meta=None,
):
    graph = module.graph
    if graph is None or not isinstance(graph, torch.fx.Graph):
        raise AssertionError("print_readable must be used on a module with a graph")

    verbose_python_code = graph.python_code(
        root_module="self",
        verbose=True,
        include_stride=include_stride,
        include_device=include_device,
        colored=colored,
        expanded_def=expanded_def,
        additional_meta=additional_meta,
    )
    module_code = verbose_python_code.src
    module_code = module_code.lstrip("\n")
    module_code = f"class {module_name}(torch.nn.Module):\n" + module_code
    module_code = _addindent(module_code, 4)

    submodule_code_list = [""]
    for submodule_name, submodule in module.named_children():
        if hasattr(submodule, "graph"):
            submodule_code_list.append(
                _print_readable(
                    submodule,
                    submodule_name,
                    print_output=False,
                    include_stride=include_stride,
                    include_device=include_device,
                    colored=colored,
                    additional_meta=additional_meta,
                )
            )
    submodule_code = "\n".join(submodule_code_list)
    submodule_code = _addindent(submodule_code, 4)

    output = module_code + submodule_code
    if print_output:
        print(module_code + submodule_code)
    return output

