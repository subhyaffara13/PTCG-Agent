
def _instantiate_template(module_interface_cls, enable_moving_cpu_tensors_to_cuda):
    instantiator.instantiate_scriptable_remote_module_template(
        module_interface_cls, enable_moving_cpu_tensors_to_cuda
    )

