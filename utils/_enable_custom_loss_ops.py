
def _enable_custom_loss_ops():
    DTensor._op_dispatcher._custom_op_handlers.update(customized_loss_ops)

