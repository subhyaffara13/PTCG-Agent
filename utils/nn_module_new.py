
def nn_module_new(cls: Any) -> Any:
    obj = object_new(cls)
    torch.nn.Module.__init__(obj)
    return obj

