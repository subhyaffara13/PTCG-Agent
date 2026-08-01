
def outputs_alias_inputs(outputs: PyTree, inputs: PyTree) -> bool:
    input_storages = {
        inp._typed_storage()._cdata
        for inp in tree_flatten_only(torch.Tensor, inputs)
        if torch._C._has_storage(inp)
    }
    return any(
        torch._C._has_storage(out) and out._typed_storage()._cdata in input_storages
        for out in tree_flatten_only(torch.Tensor, outputs)
    )

