
def _remove_activation_post_process(module):
    # TODO: maybe we should change activation_post_process to _activation_post_process
    # to prevent it from being used by user
    if hasattr(module, "activation_post_process") and _is_activation_post_process(
        module.activation_post_process
    ):
        delattr(module, "activation_post_process")

    # remove activation_post_process pre and post hooks
    def remove_hooks(pre_hook=False):
        hook_map = module._forward_pre_hooks if pre_hook else module._forward_hooks
        observer_hook = (
            _observer_forward_pre_hook if pre_hook else _observer_forward_hook
        )
        handle_ids_to_remove = set()
        for handle_id, hook_fn in hook_map.items():
            if hook_fn is observer_hook:
                handle_ids_to_remove.add(handle_id)
        for handle_id in handle_ids_to_remove:
            hook_map.pop(handle_id)

    remove_hooks(pre_hook=True)
    remove_hooks(pre_hook=False)

