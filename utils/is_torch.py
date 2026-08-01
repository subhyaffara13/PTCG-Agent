
def is_torch(filename: str) -> bool:
    dynamo_path = dynamo_dir()
    if dynamo_path is not None and filename.startswith(dynamo_path):
        return False
    torch_path = _module_dir(torch)
    return torch_path is not None and filename.startswith(torch_path)

