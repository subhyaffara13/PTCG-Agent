
def top_saved_tensors_hooks() -> Any:
    return torch._C._autograd._top_saved_tensors_default_hooks(True)

