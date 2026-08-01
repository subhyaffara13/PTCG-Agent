
def restore_torch_functions():
    torch.triu = torch_func["triu"]

