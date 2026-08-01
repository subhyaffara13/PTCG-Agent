
def _disable_custom_loss_ops():
    for custom_op in customized_loss_ops:
        DTensor._op_dispatcher._custom_op_handlers.pop(custom_op)

