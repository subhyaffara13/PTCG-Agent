
def remote_device(module_rref):
    for param in module_rref.local_value().parameters():
        return param.device

