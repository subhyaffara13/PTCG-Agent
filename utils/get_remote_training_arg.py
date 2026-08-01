
def get_remote_training_arg(module_rref):
    return module_rref.local_value().training

