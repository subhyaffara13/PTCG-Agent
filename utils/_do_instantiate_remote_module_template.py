
def _do_instantiate_remote_module_template(
    generated_module_name, str_dict, enable_moving_cpu_tensors_to_cuda
):
    if generated_module_name in sys.modules:
        return sys.modules[generated_module_name]

    loader = _StringLoader(
        get_remote_module_template(enable_moving_cpu_tensors_to_cuda).format(**str_dict)
    )
    spec = importlib.util.spec_from_loader(
        generated_module_name, loader, origin="torch-git"
    )
    if spec is None:
        raise AssertionError
    module = importlib.util.module_from_spec(spec)
    sys.modules[generated_module_name] = module
    loader.exec_module(module)
    return module

