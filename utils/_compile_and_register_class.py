
def _compile_and_register_class(obj, rcb, qualified_name):
    script_class = _get_script_class(obj)

    if not script_class:
        ast = get_jit_class_def(obj, obj.__name__)
        defaults = torch.jit.frontend.get_default_args_for_class(obj)
        script_class = torch._C._jit_script_class_compile(
            qualified_name, ast, defaults, rcb
        )
        _add_script_class(obj, script_class)

    return script_class

