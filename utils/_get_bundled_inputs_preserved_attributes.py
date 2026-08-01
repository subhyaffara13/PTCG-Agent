
def _get_bundled_inputs_preserved_attributes(script_module: torch.jit.ScriptModule, preserved_methods: list[str]) -> list[str]:

    bundled_inputs_attributes = []
    # Has bundled inputs for forward
    if hasattr(script_module, 'get_all_bundled_inputs'):
        bundled_inputs_attributes.append('get_all_bundled_inputs')
        bundled_inputs_attributes.append('get_num_bundled_inputs')

    # Bundled inputs in module after the change that introduced bundled inputs for multiple functions
    if hasattr(script_module, 'get_bundled_inputs_functions_and_info'):
        bundled_inputs_attributes.append('get_bundled_inputs_functions_and_info')
        all_info = script_module.get_bundled_inputs_functions_and_info()
        for function_name in all_info:
            if function_name not in preserved_methods:
                bundled_inputs_attributes.append(function_name)
            bundled_inputs_attributes.append("get_all_bundled_inputs_for_" + function_name)
            bundled_inputs_attributes.append("_bundled_inputs_deflated_" + function_name)

    return bundled_inputs_attributes

