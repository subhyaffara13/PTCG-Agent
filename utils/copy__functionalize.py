
def copy__functionalize(tensor, data):
    torch._sync(tensor)
    torch._sync(data)
    tensor_inner = torch._from_functional_tensor(tensor)
    data_inner = torch._from_functional_tensor(data)
    with torch._C._ExcludeDispatchKeyGuard(
        torch._C.DispatchKeySet(torch._C.DispatchKey.Functionalize)
    ):
        torch.ops.fsdp.copy_.default(tensor_inner, data_inner)

