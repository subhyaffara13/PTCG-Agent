
def _register_activation_post_process_hook(module, pre_hook=False):
    if not hasattr(module, "activation_post_process"):
        raise AssertionError(
            "Expect activation_post_process attribute already attached to the module"
        )
    if pre_hook:
        module.register_forward_pre_hook(_observer_forward_pre_hook, prepend=True)
    else:
        module.register_forward_hook(_observer_forward_hook, prepend=True)

