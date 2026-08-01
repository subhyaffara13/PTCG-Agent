
def replace_torch_functions():
    torch.triu = triu_onnx

